"""Serializers for Threat Intelligence Agent APIs."""

from rest_framework import serializers


class ThreatIntelChatSerializer(serializers.Serializer):
    """Validate threat intelligence chat requests."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    question = serializers.CharField(max_length=2000)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=10, default=5)


class ThreatIntelHistorySerializer(serializers.Serializer):
    """Validate chat history query parameters."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=25)
    offset = serializers.IntegerField(required=False, min_value=0, default=0)
