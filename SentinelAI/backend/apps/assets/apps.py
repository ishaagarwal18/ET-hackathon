"""Application configuration for assets."""

from django.apps import AppConfig


class AssetsConfig(AppConfig):
    """Assets app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.assets"
    verbose_name = "Assets"
