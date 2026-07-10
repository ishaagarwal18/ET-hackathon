"""Application configuration for behavioral anomaly APIs."""

from django.apps import AppConfig


class BehaviorConfig(AppConfig):
    """Behavior API app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.behavior"
    verbose_name = "Behavioral Anomaly Detection"
