import json

from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.http import HttpResponse
from django.urls import reverse

from .templatetags.apis_highlighter import highlight_text

from .models import Annotation

from apis_core.relations.views import CreateRelationForm


class AnnotationsView(View):
    def dispatch(self, request, *args, **kwargs):
        text_content_type = kwargs.get("text_content_type")
        text_object_id = kwargs.get("text_object_id")
        ct = ContentType.objects.get_for_id(text_content_type)
        # return 404 if not exist
        self.object = ct.get_object_for_this_type(pk=text_object_id)
        self.field_name = kwargs.get("text_field_name")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            highlight_text(self.object, request=request, field_name=self.field_name)
        )


class AnnotationDelete(DeleteView):
    model = Annotation

    def get_template_names(self):
        return ["confirm_delete", "apis_highlighter/annotation_confirm_delete.html"]

    def get_success_url(self):
        if redirect_to := self.request.GET.get("to", False):
            return redirect_to
        return super().get_success_url()


class AnnotationRelationFormView(CreateRelationForm):
    """Overload the relation form of apis_core to inject annotation data"""

    def get_form_class(self, *args, **kwargs):
        """Inject a JSONField into the form as a container for the annotation data"""
        form_class = super().get_form_class(*args, **kwargs)
        form_class.base_fields["annotationdata"] = forms.JSONField(
            widget=forms.HiddenInput()
        )
        return form_class

    def get_form_kwargs(self, *args, **kwargs) -> dict:
        """
        Set the hx-post value of the form to this view, instead of the
        default value, which is the default CreateRelationForm url of apis_core
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self.model)
        kwargs["params"]["hx_post_route"] = reverse(
            "apis_highlighter:annotation_relation", args=[content_type]
        )
        return kwargs

    def get(self, *args, **kwargs):
        """
        Add a trigger to the headers that instructs our JS to insert
        the annotation data into the form
        """
        resp = super().get(*args, **kwargs)
        trigger = json.loads(resp.get("HX-Trigger-After-Settle", "{}"))
        trigger["add_annotationdata"] = None
        resp["HX-Trigger-After-Settle"] = json.dumps(trigger)
        return resp

    def form_valid(self, form):
        """
        After saving the form (and thus the relation), use the
        annotation data to create an annotation
        """
        # we run super().form_valid so the parent class
        # runs the form save method
        resp = super().form_valid(form)
        if annotationdata := form.cleaned_data.get("annotationdata"):
            annotationdata["user"] = self.request.user
            annotationdata["object_id"] = self.object.id
            annotationdata["content_type"] = ContentType.objects.get_for_model(
                self.object
            )
            annotationdata["text_content_type"] = ContentType.objects.get_for_id(
                annotationdata["text_content_type_id"]
            )
            del annotationdata["text_content_type_id"]
            Annotation.objects.create(**annotationdata)
        return resp
