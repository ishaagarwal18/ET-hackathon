"""Serializers for health check responses."""

from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    """Health check response contract."""

    status = serializers.CharField()
    service = serializers.CharField()
    version = serializers.CharField()
    dependencies = serializers.DictField(child=serializers.CharField())
