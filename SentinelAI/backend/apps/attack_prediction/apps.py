"""Application configuration for attack prediction APIs."""

from django.apps import AppConfig


class AttackPredictionConfig(AppConfig):
    """Attack prediction app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.attack_prediction"
    verbose_name = "AI Attack Prediction"
