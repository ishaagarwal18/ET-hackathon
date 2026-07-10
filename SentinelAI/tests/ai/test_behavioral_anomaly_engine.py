"""AI model tests for the Behavioral Anomaly Detection Engine."""

import pytest

from ai_engines.behavioral_anomaly.explainability import calculate_risk_score
from ai_engines.behavioral_anomaly.features import extract_features, feature_vector
from ai_engines.behavioral_anomaly.services import engine as engine_module
from ai_engines.behavioral_anomaly.training.synthetic import generate_synthetic_user_activity


pytestmark = pytest.mark.ai


class InMemoryProfileRepository:
    def __init__(self):
        self.saved = []

    def upsert_profile(self, **kwargs):
        self.saved.append(kwargs)
        return "profile-test-001"


class DeterministicModel:
    def analyze(self, feature_row):
        return {"is_anomaly": True, "decision_score": -0.31, "anomaly_score": 0.81}


def test_feature_extraction_canonicalizes_behavior_payload(load_mock_data):
    payload = load_mock_data("behavior_activity.json")

    features = extract_features(payload)
    vector = feature_vector(features)

    assert features["is_off_hours"] == 1.0
    assert features["location_risk"] == 1.0
    assert features["failed_login_count"] == 7.0
    assert len(vector) == len(features)


def test_risk_score_increases_with_high_risk_signals(load_mock_data):
    features = extract_features(load_mock_data("behavior_activity.json"))

    score = calculate_risk_score(features, anomaly_score=0.81)

    assert 80 <= score <= 100


def test_synthetic_training_data_has_expected_width():
    rows = generate_synthetic_user_activity(size=50, seed=7)

    assert len(rows) >= 50
    assert {len(row) for row in rows} == {9}


def test_behavior_service_persists_profile_without_real_mongodb(monkeypatch, load_mock_data):
    repository = InMemoryProfileRepository()
    monkeypatch.setattr(engine_module, "get_trained_isolation_forest", lambda: DeterministicModel())

    service = engine_module.BehavioralAnomalyDetectionService(repository=repository)
    payload = load_mock_data("behavior_activity.json")
    result = service.analyze(
        tenant_id=payload["tenant_id"],
        user_identifier=payload["user_identifier"],
        payload={k: v for k, v in payload.items() if k not in {"tenant_id", "user_identifier"}},
    )

    assert result["profile_id"] == "profile-test-001"
    assert result["is_anomaly"] is True
    assert result["confidence_score"] > 0
    assert repository.saved[0]["profile"]["metadata"]["lstm_integration_ready"] is True
