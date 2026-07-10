"""Serializers for AI Attack Prediction Agent APIs."""

from rest_framework import serializers

from agents.attack_prediction.constants import ATTACK_STAGES


class AttackPredictionSerializer(serializers.Serializer):
    """Validate attack prediction input."""

    anomaly = serializers.DictField()
    mitre_technique = serializers.CharField(max_length=255)
    current_stage = serializers.ChoiceField(choices=ATTACK_STAGES)
    previous_activities = serializers.ListField(
        child=serializers.CharField(max_length=500),
        allow_empty=True,
        max_length=100,
    )

    def validate_anomaly(self, value):
        """Require a numeric anomaly score in the anomaly payload."""
        score = value.get("anomaly_score", value.get("score"))
        if score is None:
            raise serializers.ValidationError("anomaly_score or score is required.")
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Anomaly score must be numeric.") from None
        if numeric_score < 0 or numeric_score > 1:
            raise serializers.ValidationError("Anomaly score must be between 0 and 1.")
        return value
