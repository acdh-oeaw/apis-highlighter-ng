from django.urls import path

from . import views

app_name = "apis_highlighter"

urlpatterns = [
    path(
        "annotations/<text_content_type>/<text_object_id>",
        views.AnnotationsView.as_view(),
        name="annotations",
    ),
    path(
        "annotations/<text_content_type>/<text_object_id>/<project_id>",
        views.AnnotationsView.as_view(),
        name="annotations",
    ),
]
