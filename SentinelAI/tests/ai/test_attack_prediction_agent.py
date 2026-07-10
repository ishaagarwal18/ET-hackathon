"""AI agent tests for attack prediction."""

import pytest

from agents.attack_prediction.services.predictor import AttackPredictionService


pytestmark = pytest.mark.ai


def test_attack_prediction_returns_ranked_defensive_recommendation(load_mock_data):
    payload = load_mock_data("attack_prediction.json")

    result = AttackPredictionService().predict(**payload)

    assert result["likely_next_attack"] == "Internal discovery using valid accounts"
    assert result["predicted_stage"] == "discovery"
    assert 0 < result["probability"] <= 0.97
    assert "recommended_defense" in result
    assert result["attack_chain_visualization"]["nodes"]


def test_attack_prediction_serializer_rejects_out_of_range_anomaly():
    from apps.attack_prediction.serializers import AttackPredictionSerializer

    serializer = AttackPredictionSerializer(
        data={
            "anomaly": {"anomaly_score": 1.5},
            "mitre_technique": "T1059 Command and Scripting Interpreter",
            "current_stage": "execution",
            "previous_activities": [],
        }
    )

    assert serializer.is_valid() is False
    assert "anomaly" in serializer.errors
