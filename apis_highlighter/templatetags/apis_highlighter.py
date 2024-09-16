from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.urls import reverse
from apis_highlighter.models import Annotation, AnnotationProject
from apis_highlighter.helpers import get_annotation_project

register = template.Library()


def overlap(range_one, range_two) -> bool:
    r = range(max(range_one[0], range_two[0]), min(range_one[1], range_two[1]))
    return bool(r)


@register.simple_tag
def highlight_text(obj, request=None, field_name="text"):
    project_id = get_annotation_project(request)

    ct = ContentType.objects.get_for_model(obj)
    annotations = Annotation.objects.filter(
        text_content_type=ct, text_object_id=obj.id, text_field_name=field_name
    )
    args = [ct.id, obj.id, field_name]
    if project_id:
        annotations = annotations.filter(project__id=project_id)
        args.append(project_id)

    annotations_url = reverse("apis_highlighter:annotations", args=args)
    prefix = (
        f"<div class='highlight-text'"
        f" data-text_object_id='{obj.id}'"
        f" data-text_content_type_id='{ct.id}'"
        f" data-text_field_name='{field_name}'"
        f" data-project_id='{project_id}'"
        f" data-source='{annotations_url}'>"
    )
    suffix = "</div>"

    text = getattr(obj, field_name)
    annotated_ranges = []
    for ann in annotations.order_by("-start"):
        if not any(map(lambda x: overlap((ann.start, ann.end), x), annotated_ranges)):
            content_object = escape(ann.content_object)
            orig_string = escape(ann.orig_string)
            annotated_ranges.append((ann.start, ann.end))
            title = (
                f'Annotation "{orig_string}" '
                + f"from {ann.user} in project {ann.project}; "
                + f"pointing to {content_object}"
            )
            end = ann.end
            start = ann.start
            text = text[:end] + "</mark>" + text[end:]
            annotation_delete_url = reverse(
                "apis_highlighter:annotationdelete",
                args=[
                    ann.id,
                ],
            )
            text = (
                text[:start]
                + f"<mark data-ann-id='{ann.id}' "
                + f"title='{title}' "
                + f"data-hl-start='{ann.start}' "
                + f"data-hl-end='{ann.end}' "
                + f"data-hl-orig_string='{orig_string}' "
                + f"data-hl-text-id='{content_object}' "
                + f"data-delete='{annotation_delete_url}' "
                + "onclick='annotation_menu(this)' >"
                + text[start:]
            )
        else:
            print(f"Annotation is overlapping: {ann}")
    text = text.replace("\n", "<br/>")

    return mark_safe(prefix + text + suffix)


@register.inclusion_tag("apis_highlighter/select_project.html")
def select_highlighter_project(request):
    project_id = get_annotation_project(request)
    return {
        "request": request,
        "projects": AnnotationProject.objects.all(),
        "project_id": project_id,
    }
