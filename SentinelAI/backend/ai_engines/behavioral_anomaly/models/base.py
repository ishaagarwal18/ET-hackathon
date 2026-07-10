"""Model adapter contracts for behavioral anomaly detection."""

from abc import ABC, abstractmethod


class BehavioralAnomalyModel(ABC):
    """Interface for current and future behavioral anomaly models."""

    @abstractmethod
    def train(self, training_rows: list[list[float]]) -> None:
        """Train the model adapter."""

    @abstractmethod
    def analyze(self, feature_row: list[float]) -> dict:
        """Analyze one feature row and return model scores."""


class FutureLSTMBehaviorModel(BehavioralAnomalyModel):
    """Placeholder contract for future sequence-based LSTM integration."""

    def train(self, training_rows: list[list[float]]) -> None:
        raise NotImplementedError("LSTM training will be implemented in a sequence-model adapter.")

    def analyze(self, feature_row: list[float]) -> dict:
        raise NotImplementedError("LSTM inference will be implemented in a sequence-model adapter.")
