"""Scoring algorithm for attack prediction."""


class AttackPredictionScorer:
    """Convert candidate scores into probabilities."""

    def score_candidates(self, candidates: list[tuple], graph) -> list[dict]:
        """Return normalized predictions."""
        enriched = []
        for rule, score in candidates:
            score += graph.graph_boost(rule.current_stage, rule.next_stage)
            enriched.append((rule, max(score, 0.01)))

        total = sum(score for _, score in enriched) or 1.0
        predictions = []
        for rule, score in enriched:
            probability = round(min(score / total, 0.97), 4)
            predictions.append(
                {
                    "rule": rule.name,
                    "likely_next_attack": rule.next_attack,
                    "next_stage": rule.next_stage,
                    "probability": probability,
                    "recommended_defense": rule.defense,
                }
            )
        return sorted(predictions, key=lambda item: item["probability"], reverse=True)
