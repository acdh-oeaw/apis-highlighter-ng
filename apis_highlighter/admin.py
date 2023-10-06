from django.contrib import admin
from .models import Annotation, AnnotationProject


@admin.register(Annotation, AnnotationProject)
class HighlighterAdmin(admin.ModelAdmin):
    pass
