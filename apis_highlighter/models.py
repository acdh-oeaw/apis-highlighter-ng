from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AnnotationProject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Annotation(models.Model):
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    orig_string = models.CharField(max_length=255, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    text_content_type = models.ForeignKey(
        ContentType,
        related_name="text_annotation_set",
        on_delete=models.CASCADE,
        null=True,
    )
    text_object_id = models.PositiveIntegerField(null=True)
    text_content_object = GenericForeignKey("text_content_type", "text_object_id")
    text_field_name = models.CharField(default="text")

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    project = models.ForeignKey(
        AnnotationProject, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Annotation "{self.orig_string}" to {self.content_object}'
