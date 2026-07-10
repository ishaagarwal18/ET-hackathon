"""Serializers for users."""

from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only user representation for API responses."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_verified",
            "date_joined",
        )
        read_only_fields = fields
