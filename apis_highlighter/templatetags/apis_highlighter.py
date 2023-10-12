from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.urls import reverse
from apis_highlighter.models import Annotation, AnnotationProject

register = template.Library()


def overlap(range_one, range_two) -> bool:
    r = range(max(range_one[0], range_two[0]), min(range_one[-1], range_two[-1]))
    return bool(r)


@register.filter()
def highlight_text(obj, request=None, fieldname="text", project_id=None):
    if project_id is None:
        default_project = getattr(settings, "DEFAULT_HIGHLIGTHER_PROJECT", None)
        project_id = request.GET.get("highlighter_project", default_project)

    ct = ContentType.objects.get_for_model(obj)
    annotations = Annotation.objects.filter(text_content_type=ct, text_object_id=obj.id)
    args = [ct.id, obj.id]
    if project_id:
        annotations = annotations.filter(project__id=project_id)
        args.append(project_id)

    annotations_url = reverse("apis_highlighter:annotations", args=args)
    prefix = (
        f"<div class='highlight-text'"
        f" data-text_object_id='{obj.id}'"
        f" data-text_content_type_id='{ct.id}'"
        f" data-project_id='{project_id}'"
        f" data-source='{annotations_url}'>"
    )
    suffix = "</div>"

    text = getattr(obj, fieldname)
    annotated_ranges = []
    for ann in annotations.order_by("-start"):
        if not any(
            map(lambda x: overlap(range(ann.start, ann.end), x), annotated_ranges)
        ):
            annotated_ranges.append(range(ann.start, ann.end))
            title = (
                f'Annotation "{ann.orig_string}" '
                + f"from {ann.user} in project {ann.project}; "
                + f"pointing to {ann.content_object}"
            )
            end = ann.end
            start = ann.start
            text = text[:end] + "</mark>" + text[end:]
            text = (
                text[:start]
                + f"<mark data-ann-id='{ann.id}' "
                + f"title='{title}' "
                + f"data-hl-start='{ann.start}' "
                + f"data-hl-end='{ann.end}' "
                + f"data-hl-orig_string='{ann.orig_string}' "
                + f"data-hl-text-id='{ann.content_object}'>"
                + text[start:]
            )
        else:
            print(f"Annotation is overlapping: {ann}")
    text = text.replace("\n", "<br/>")

    return mark_safe(prefix + text + suffix)


@register.inclusion_tag("apis_highlighter/select_project.html")
def select_highlighter_project(request):
    return {"request": request, "projects": AnnotationProject.objects.all()}
