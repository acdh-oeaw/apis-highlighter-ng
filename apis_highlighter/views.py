import json

from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from .templatetags.apis_highlighter import highlight_text

from .models import Annotation

from apis_core.apis_relations.models import TempTriple


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
        return HttpResponse(highlight_text(self.object, field_name=self.field_name))


class AnnotationDelete(DeleteView):
    model = Annotation

    def get_template_names(self):
        return ["confirm_delete", "apis_highlighter/annotation_confirm_delete.html"]

    def get_success_url(self):
        if redirect_to := self.request.GET.get("to", False):
            return redirect_to
        return super().get_success_url()


# wrapper around the `save_ajax_form` method from apis_relations.views
# this lets us create the annotation while creating the relation
def save_ajax_form(
    request, entity_type, kind_form, SiteID, ObjectID=False, annotationdata=None
):
    from apis_core.apis_relations.views import save_ajax_form as orig_save_ajax_form

    resp = orig_save_ajax_form(request, entity_type, kind_form, SiteID, ObjectID)
    data = json.loads(resp.content.decode())
    if annotationdata := request.POST.get("annotationdata"):
        annotationdata = json.loads(annotationdata)
        annotationdata["user"] = request.user
        annotationdata["object_id"] = data["instance"]["relation_pk"]
        annotationdata["content_type"] = ContentType.objects.get_for_model(TempTriple)
        annotationdata["text_content_type"] = ContentType.objects.get_for_id(
            annotationdata["text_content_type_id"]
        )
        del annotationdata["text_content_type_id"]
        Annotation.objects.create(**annotationdata)
    return resp
