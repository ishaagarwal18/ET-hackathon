"""Application configuration for threat intelligence APIs."""

from django.apps import AppConfig


class ThreatIntelligenceConfig(AppConfig):
    """Threat intelligence app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.threat_intelligence"
    verbose_name = "Threat Intelligence"
