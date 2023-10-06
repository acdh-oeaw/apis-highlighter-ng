from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from .templatetags.apis_highlighter import highlight_text


class AnnotationsView(View):
    def dispatch(self, request, *args, **kwargs):
        text_content_type = kwargs.get("text_content_type")
        text_object_id = kwargs.get("text_object_id")
        ct = ContentType.objects.get_for_id(text_content_type)
        # return 404 if not exist
        self.object = ct.get_object_for_this_type(pk=text_object_id)
        self.project_id = kwargs.get("project_id")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse(highlight_text(self.object, self.project_id))
