"""Serializers for AI SOC Assistant APIs."""

from rest_framework import serializers


class SOCAssistantChatSerializer(serializers.Serializer):
    """Validate SOC Assistant chat requests."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    message = serializers.CharField(max_length=4000)
    context = serializers.DictField(required=False, default=dict)


class SOCAssistantHistorySerializer(serializers.Serializer):
    """Validate SOC Assistant history query parameters."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=25)
    offset = serializers.IntegerField(required=False, min_value=0, default=0)
