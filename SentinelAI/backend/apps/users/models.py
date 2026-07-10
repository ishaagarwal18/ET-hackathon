"""Data models for users."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extensible platform user model."""

    class Role(models.TextChoices):
        """Supported SentinelAI platform roles."""

        SOC_ANALYST = "soc_analyst", "SOC Analyst"
        SECURITY_ADMIN = "security_admin", "Security Admin"
        GOVERNMENT_OFFICER = "government_officer", "Government Officer"
        READ_ONLY_AUDITOR = "read_only_auditor", "Read Only Auditor"

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.SOC_ANALYST)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.get_username()
