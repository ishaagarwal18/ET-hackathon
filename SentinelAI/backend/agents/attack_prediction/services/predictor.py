"""Attack prediction application service."""

from agents.attack_prediction.graph.knowledge_graph import AttackKnowledgeGraph
from agents.attack_prediction.rules.rule_engine import AttackPredictionRuleEngine
from agents.attack_prediction.scoring.scorer import AttackPredictionScorer
from agents.attack_prediction.visualization.attack_chain import build_attack_chain_visualization


class AttackPredictionService:
    """Predict likely next attack step from anomaly and ATT&CK context."""

    def __init__(self, rule_engine=None, graph=None, scorer=None):
        self.rule_engine = rule_engine or AttackPredictionRuleEngine()
        self.graph = graph or AttackKnowledgeGraph()
        self.scorer = scorer or AttackPredictionScorer()

    def predict(
        self,
        *,
        anomaly: dict,
        mitre_technique: str,
        current_stage: str,
        previous_activities: list[str],
    ) -> dict:
        """Return the most likely next attack and supporting context."""
        anomaly_score = float(anomaly.get("anomaly_score", anomaly.get("score", 0.0)))
        candidates = self.rule_engine.evaluate(
            current_stage=current_stage,
            mitre_technique=mitre_technique,
            previous_activities=previous_activities,
            anomaly_score=anomaly_score,
        )
        predictions = self.scorer.score_candidates(candidates, self.graph)
        top_prediction = predictions[0]
        visualization = build_attack_chain_visualization(
            current_stage=current_stage,
            prediction=top_prediction,
            previous_activities=previous_activities,
        )

        return {
            "likely_next_attack": top_prediction["likely_next_attack"],
            "probability": top_prediction["probability"],
            "recommended_defense": top_prediction["recommended_defense"],
            "mitre_technique": mitre_technique,
            "current_stage": current_stage,
            "predicted_stage": top_prediction["next_stage"],
            "ranked_predictions": predictions[:5],
            "attack_chain_visualization": visualization,
            "explanation": [
                f"Current stage '{current_stage}' was evaluated against the attack knowledge graph.",
                f"MITRE technique context '{mitre_technique}' influenced rule matching.",
                f"Anomaly score {round(anomaly_score, 4)} increased confidence in near-term progression.",
            ],
        }
