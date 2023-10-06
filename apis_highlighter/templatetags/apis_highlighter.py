from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from apis_highlighter.models import Annotation

register = template.Library()


@register.filter()
def highlight_text(obj, project_id=None):
    ct = ContentType.objects.get_for_model(obj)
    annotations = Annotation.objects.filter(text_content_type=ct, text_object_id=obj.id)
    if project_id:
        annotations = annotations.filter(project__id=project_id)

    text = obj.text
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
    return mark_safe(text)
