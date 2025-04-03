# Generated by Django 5.1.7 on 2025-04-01 01:49

import app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoredFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to=app.models.file_upload_path)),
                ("file_bytes", models.PositiveIntegerField(blank=True, null=True)),
                ("views", models.PositiveIntegerField(default=0)),
                ("is_public", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "public_link",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
