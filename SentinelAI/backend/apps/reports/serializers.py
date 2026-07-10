"""Serializers for reports."""

from rest_framework import serializers


class TimelineEventSerializer(serializers.Serializer):
    """Incident report timeline event."""

    timestamp = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=1000)


class MITREMappingSerializer(serializers.Serializer):
    """MITRE ATT&CK mapping item."""

    technique_id = serializers.CharField(max_length=32)
    technique_name = serializers.CharField(max_length=255)
    tactic = serializers.CharField(max_length=255)


class AffectedAssetSerializer(serializers.Serializer):
    """Affected asset report item."""

    asset_id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    criticality = serializers.CharField(max_length=64)


class ResponseActionSerializer(serializers.Serializer):
    """Response action report item."""

    action = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=64)
    details = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class RecommendationSerializer(serializers.Serializer):
    """Recommendation report item."""

    priority = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=1000)


class IncidentReportSerializer(serializers.Serializer):
    """Validate incident report generation input."""

    tenant_id = serializers.CharField(required=False, allow_blank=True, max_length=64)
    formats = serializers.ListField(
        child=serializers.ChoiceField(choices=("pdf", "csv", "json")),
        min_length=1,
        max_length=3,
        default=["pdf", "csv", "json"],
    )
    classification = serializers.CharField(required=False, allow_blank=True, max_length=64)
    executive_summary = serializers.CharField(max_length=5000)
    incident = serializers.DictField()
    risk_score = serializers.DictField()
    timeline = TimelineEventSerializer(many=True, required=False)
    mitre_mapping = MITREMappingSerializer(many=True, required=False)
    affected_assets = AffectedAssetSerializer(many=True, required=False)
    response_actions = ResponseActionSerializer(many=True, required=False)
    recommendations = RecommendationSerializer(many=True, required=False)

    def validate_incident(self, value):
        required = ("incident_id", "title", "severity", "status")
        missing = [field for field in required if not value.get(field)]
        if missing:
            raise serializers.ValidationError(f"Missing incident fields: {', '.join(missing)}")
        return value

    def validate_risk_score(self, value):
        if "score" not in value or "level" not in value:
            raise serializers.ValidationError("risk_score requires score and level.")
        return value
