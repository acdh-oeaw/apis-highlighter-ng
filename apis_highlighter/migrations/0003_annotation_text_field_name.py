# Generated by Django 4.2.10 on 2024-03-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "apis_highlighter",
            "0002_rename_annotation_project_annotation_project_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="text_field_name",
            field=models.CharField(default="text"),
        ),
    ]
