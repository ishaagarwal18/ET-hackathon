"""Application configuration for incidents."""

from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    """Incidents app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.incidents"
    verbose_name = "Incidents"
