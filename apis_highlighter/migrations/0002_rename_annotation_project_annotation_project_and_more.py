# Generated by Django 4.1.11 on 2023-10-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis_highlighter", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="annotation",
            old_name="annotation_project",
            new_name="project",
        ),
        migrations.AddField(
            model_name="annotation",
            name="orig_string",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
