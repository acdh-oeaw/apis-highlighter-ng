from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from .models import Annotation


class AnnotationsView(View):
    annotations = None

    def dispatch(self, request, *args, **kwargs):
        text_content_type = kwargs.get("text_content_type")
        text_object_id = kwargs.get("text_object_id")
        ct = ContentType.objects.get_for_id(text_content_type)
        # return 404 if not exist
        self.object = ct.get_object_for_this_type(pk=text_object_id)

        self.annotations = Annotation.objects.filter(
            text_content_type=ct, text_object_id=text_object_id
        )

        if project_id := kwargs.get("project_id"):
            self.annotations = self.annotations.filter(project__id=project_id)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.highlight(self.object.text, self.annotations))

    def highlight(self, text, annotations):
        for ann in annotations.order_by("-start"):
            text = text[: ann.end] + "</mark>" + text[ann.end :]
            text = (
                text[: ann.start]
                + f"<mark data-ann-id='{ann.id}' "
                + f"data-hl-start='{ann.start}' "
                + f"data-hl-end='{ann.end}' "
                + f"data-hl-text-id='{ann.content_object}'>"
                + text[ann.start :]
            )
        return text
