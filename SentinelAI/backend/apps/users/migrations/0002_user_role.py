# Generated for SentinelAI role-based access control.

from django.db import migrations, models


class Migration(migrations.Migration):
    """Add platform role support to users."""

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("soc_analyst", "SOC Analyst"),
                    ("security_admin", "Security Admin"),
                    ("government_officer", "Government Officer"),
                    ("read_only_auditor", "Read Only Auditor"),
                ],
                default="soc_analyst",
                max_length=32,
            ),
        ),
    ]
