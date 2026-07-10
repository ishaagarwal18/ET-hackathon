"""Application configuration for alerts."""

from django.apps import AppConfig


class AlertsConfig(AppConfig):
    """Alerts app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.alerts"
    verbose_name = "Alerts"
