"""Serializers for incidents."""

from rest_framework import serializers

from agents.incident_response.constants import RISK_LEVELS


class IncidentResponseApprovalSerializer(serializers.Serializer):
    """Validate approval workflow input."""

    approved = serializers.BooleanField(required=False, default=False)
    approved_by = serializers.CharField(required=False, allow_blank=True, max_length=255)
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)


class AutonomousIncidentResponseSerializer(serializers.Serializer):
    """Validate autonomous incident response request."""

    risk_level = serializers.ChoiceField(choices=RISK_LEVELS)
    incident = serializers.DictField()
    approval = IncidentResponseApprovalSerializer(required=False)

    def validate_incident(self, value):
        """Require minimum incident identity context."""
        if not value.get("incident_id"):
            raise serializers.ValidationError("incident_id is required.")
        return value
