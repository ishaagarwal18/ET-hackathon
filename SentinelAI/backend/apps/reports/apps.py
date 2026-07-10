"""Application configuration for reports."""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Reports app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
    verbose_name = "Reports"
