"""Attack-chain knowledge graph."""

from agents.attack_prediction.constants import DEFAULT_DEFENSES, STAGE_ORDER


class AttackKnowledgeGraph:
    """Represent likely progression between attack stages."""

    EDGES = {
        "reconnaissance": ("initial_access",),
        "initial_access": ("execution", "discovery", "persistence"),
        "execution": ("persistence", "privilege_escalation", "defense_evasion"),
        "persistence": ("privilege_escalation", "credential_access"),
        "privilege_escalation": ("defense_evasion", "credential_access", "discovery"),
        "defense_evasion": ("credential_access", "discovery", "command_and_control"),
        "credential_access": ("discovery", "lateral_movement"),
        "discovery": ("lateral_movement", "collection"),
        "lateral_movement": ("collection", "command_and_control"),
        "collection": ("exfiltration", "impact"),
        "command_and_control": ("collection", "exfiltration", "impact"),
        "exfiltration": ("impact",),
        "impact": (),
    }

    def next_stages(self, stage: str) -> tuple[str, ...]:
        """Return graph neighbors for a stage."""
        return self.EDGES.get(stage, ())

    def graph_boost(self, current_stage: str, next_stage: str) -> float:
        """Return a score boost for graph-supported progression."""
        if next_stage in self.next_stages(current_stage):
            return 0.18
        if STAGE_ORDER.get(next_stage, 0) > STAGE_ORDER.get(current_stage, 0):
            return 0.06
        return -0.05

    def defense_for_stage(self, stage: str) -> str:
        """Return default defense guidance for a stage."""
        return DEFAULT_DEFENSES.get(stage, "Increase monitoring, preserve evidence, and escalate to incident response.")
