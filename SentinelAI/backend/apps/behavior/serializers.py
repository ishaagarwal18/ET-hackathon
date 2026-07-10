"""Serializers for behavioral anomaly detection."""

from rest_framework import serializers


class AnalyzeBehaviorSerializer(serializers.Serializer):
    """Validate behavioral anomaly analysis input."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    user_identifier = serializers.CharField(max_length=255)
    login_time = serializers.CharField(max_length=64)
    location = serializers.CharField(max_length=255)
    ip = serializers.IPAddressField()
    failed_login_count = serializers.IntegerField(min_value=0, max_value=10000)
    usb_activity = serializers.BooleanField()
    download_size = serializers.FloatField(min_value=0)
    file_access = serializers.IntegerField(min_value=0)
    process_creation = serializers.IntegerField(min_value=0)
