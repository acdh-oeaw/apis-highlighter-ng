from django.urls import path, re_path

from . import views

app_name = "apis_highlighter"

urlpatterns = [
    path(
        "annotations/<text_content_type>/<text_object_id>/<text_field_name>",
        views.AnnotationsView.as_view(),
        name="annotations",
    ),
    path(
        "annotations/<text_content_type>/<text_object_id>/<text_field_name>/<project_id>",
        views.AnnotationsView.as_view(),
        name="annotations",
    ),
    path(
        "annotation/<int:pk>/delete",
        views.AnnotationDelete.as_view(),
        name="annotationdelete",
    ),
    re_path(
        r"apis/relations/ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)(?:/(?P<ObjectID>[0-9]*))?/$",
        views.save_ajax_form,
        name="save_ajax_form",
    ),
]
