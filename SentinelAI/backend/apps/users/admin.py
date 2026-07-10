"""Admin registration for users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class SentinelAIUserAdmin(UserAdmin):
    """Django admin configuration for the SentinelAI user model."""

    fieldsets = UserAdmin.fieldsets + (
        ("SentinelAI", {"fields": ("role", "is_verified")}),
    )
    list_display = ("username", "email", "role", "is_active", "is_staff", "is_verified")
    list_filter = UserAdmin.list_filter + ("role", "is_verified")
    search_fields = ("username", "email", "first_name", "last_name")
