"""Isolation Forest model adapter."""

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ai_engines.behavioral_anomaly.models.base import BehavioralAnomalyModel


class IsolationForestBehaviorModel(BehavioralAnomalyModel):
    """Scikit-learn Isolation Forest adapter for user activity analysis."""

    def __init__(self, contamination: float = 0.06, random_state: int = 42):
        self.pipeline = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    IsolationForest(
                        n_estimators=250,
                        contamination=contamination,
                        random_state=random_state,
                        n_jobs=-1,
                    ),
                ),
            ]
        )
        self.is_trained = False

    def train(self, training_rows: list[list[float]]) -> None:
        """Train the Isolation Forest pipeline."""
        self.pipeline.fit(training_rows)
        self.is_trained = True

    def analyze(self, feature_row: list[float]) -> dict:
        """Return anomaly decision and raw anomaly score."""
        if not self.is_trained:
            raise RuntimeError("Behavioral anomaly model has not been trained.")

        prediction = int(self.pipeline.predict([feature_row])[0])
        decision_score = float(self.pipeline.decision_function([feature_row])[0])
        anomaly_score = max(0.0, min(1.0, 0.5 - decision_score))
        return {
            "is_anomaly": prediction == -1,
            "decision_score": decision_score,
            "anomaly_score": round(anomaly_score, 4),
        }
