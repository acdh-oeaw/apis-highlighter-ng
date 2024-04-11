from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import Annotation
from .helpers import correlate_annotations

APP_LABEL_EXCLUDE = ["admin", "auth", "sessions", "apis_highlighter"]


@receiver(pre_save)
def update_annotations_offsets(sender, instance, raw, using, update_fields, **kwargs):
    meta = getattr(sender, "_meta", {})
    app_label = getattr(meta, "app_label", "apis_highlighter")
    if app_label not in APP_LABEL_EXCLUDE:
        if getattr(instance, "id", False):
            content_type = ContentType.objects.get_for_model(instance)
            annotations = Annotation.objects.filter(
                text_content_type=content_type, text_object_id=instance.id
            ).order_by("start")
            if annotations:
                object_pre_save = sender.objects.get(id=instance.id)
                annotated_fields = set(
                    annotations.values_list("text_field_name", flat=True)
                )
                for field_name in annotated_fields:
                    text_pre_save = getattr(object_pre_save, field_name)
                    text_post_save = getattr(instance, field_name)
                    if text_pre_save != text_post_save:
                        correlate_annotations(
                            text_old=text_pre_save,
                            text_new=text_post_save,
                            annotations_old=annotations,
                        )
