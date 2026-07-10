"""Application configuration for MongoDB operations."""

from django.apps import AppConfig


class CoreMongodbConfig(AppConfig):
    """Core MongoDB app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core_mongodb"
    verbose_name = "Core MongoDB"
