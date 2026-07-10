"""Serializers for dashboard."""

from rest_framework import serializers


class DashboardTenantSerializer(serializers.Serializer):
    """Common dashboard tenant query parameters."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)


class DashboardLimitSerializer(DashboardTenantSerializer):
    """Validate limit-based dashboard widgets."""

    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)


class DashboardTimelineSerializer(DashboardTenantSerializer):
    """Validate attack timeline query parameters."""

    hours = serializers.IntegerField(required=False, min_value=1, max_value=168, default=24)
