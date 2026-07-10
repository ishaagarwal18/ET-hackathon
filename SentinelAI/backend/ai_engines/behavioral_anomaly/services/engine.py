"""Behavioral anomaly detection application service."""

from functools import lru_cache

from ai_engines.behavioral_anomaly.constants import DEFAULT_SYNTHETIC_TRAINING_SIZE
from ai_engines.behavioral_anomaly.explainability import (
    build_explanation,
    calculate_confidence_score,
    calculate_risk_score,
)
from ai_engines.behavioral_anomaly.features import extract_features, feature_vector
from ai_engines.behavioral_anomaly.models.isolation_forest import IsolationForestBehaviorModel
from ai_engines.behavioral_anomaly.repositories.profile_repository import BehaviorProfileRepository
from ai_engines.behavioral_anomaly.training.synthetic import generate_synthetic_user_activity


@lru_cache(maxsize=1)
def get_trained_isolation_forest() -> IsolationForestBehaviorModel:
    """Return a cached Isolation Forest trained on synthetic baseline activity."""
    model = IsolationForestBehaviorModel()
    training_rows = generate_synthetic_user_activity(DEFAULT_SYNTHETIC_TRAINING_SIZE)
    model.train(training_rows)
    return model


class BehavioralAnomalyDetectionService:
    """Analyze user activity and persist behavior profile updates."""

    def __init__(self, repository: BehaviorProfileRepository | None = None):
        self.repository = repository or BehaviorProfileRepository()
        self.model = get_trained_isolation_forest()

    def analyze(self, *, tenant_id: str, user_identifier: str, payload: dict) -> dict:
        """Analyze activity, score risk, explain result, and store behavior profile."""
        features = extract_features(payload)
        vector = feature_vector(features)
        model_result = self.model.analyze(vector)
        risk_score = calculate_risk_score(features, model_result["anomaly_score"])
        confidence_score = calculate_confidence_score(features, model_result["anomaly_score"])
        explanation = build_explanation(features, model_result)

        profile = {
            "user_identifier": user_identifier,
            "risk_score": risk_score,
            "anomaly_score": model_result["anomaly_score"],
            "confidence_score": confidence_score,
            "is_anomaly": model_result["is_anomaly"],
            "features": features,
            "statistics": {
                "decision_score": model_result["decision_score"],
                "training_source": "synthetic_baseline",
                "model_family": "isolation_forest",
            },
            "explanation": explanation,
            "last_activity": payload,
            "baseline_window_days": 30,
            "metadata": {
                "lstm_integration_ready": True,
                "sequence_features_pending": True,
            },
        }
        profile_id = self.repository.upsert_profile(
            tenant_id=tenant_id,
            user_identifier=user_identifier,
            profile=profile,
        )

        return {
            "profile_id": profile_id,
            "user_identifier": user_identifier,
            "risk_score": risk_score,
            "anomaly_score": model_result["anomaly_score"],
            "confidence_score": confidence_score,
            "is_anomaly": model_result["is_anomaly"],
            "explanation": explanation,
            "features": features,
        }
