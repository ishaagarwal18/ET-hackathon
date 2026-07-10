"""Application configuration for logs."""

from django.apps import AppConfig


class LogsConfig(AppConfig):
    """Logs app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.logs"
    verbose_name = "Logs"
