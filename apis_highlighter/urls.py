from django.urls import path

from . import views

app_name = "apis_highlighter"

urlpatterns = [
    path(
        "annotations/<text_content_type>/<text_object_id>/<text_field_name>",
        views.AnnotationsView.as_view(),
        name="annotations",
    ),
    path(
        "annotation/<int:pk>/delete",
        views.AnnotationDelete.as_view(),
        name="annotationdelete",
    ),
    path(
        "annotation/relation/<contenttype:contenttype>/form",
        views.AnnotationRelationFormView.as_view(),
        name="annotation_relation",
    ),
]
