"""Serializers for logs."""

from rest_framework import serializers

from agents.log_collector.constants import SUPPORTED_LOG_SOURCES


class UploadLogSerializer(serializers.Serializer):
    """Validate log upload requests."""

    source_type = serializers.ChoiceField(choices=SUPPORTED_LOG_SOURCES)
    source_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    file = serializers.FileField(required=False)
    content = serializers.CharField(required=False, allow_blank=False, trim_whitespace=False)

    def validate(self, attrs):
        """Require either file upload or inline content."""
        if not attrs.get("file") and not attrs.get("content"):
            raise serializers.ValidationError("Provide either a log file or inline content.")
        return attrs


class ListLogsSerializer(serializers.Serializer):
    """Validate list log query parameters."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    source_type = serializers.ChoiceField(choices=SUPPORTED_LOG_SOURCES, required=False)
    severity = serializers.ChoiceField(
        choices=("informational", "low", "medium", "high", "critical"),
        required=False,
    )
    status = serializers.CharField(required=False, max_length=64)
    limit = serializers.IntegerField(default=50, min_value=1, max_value=500)
    offset = serializers.IntegerField(default=0, min_value=0)


class LogDetailsSerializer(serializers.Serializer):
    """Validate log detail query parameters."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    log_id = serializers.CharField(max_length=24, min_length=24)
