"""Application configuration for AI SOC Assistant APIs."""

from django.apps import AppConfig


class SOCAssistantConfig(AppConfig):
    """SOC Assistant app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.soc_assistant"
    verbose_name = "AI SOC Assistant"
