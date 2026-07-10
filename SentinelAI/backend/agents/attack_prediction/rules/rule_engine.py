"""Deterministic rule engine for next-attack prediction."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AttackRule:
    """A transparent prediction rule."""

    name: str
    current_stage: str
    next_attack: str
    next_stage: str
    mitre_patterns: tuple[str, ...]
    activity_patterns: tuple[str, ...]
    base_weight: float
    defense: str

    def score(self, *, mitre_technique: str, previous_activities: list[str], anomaly_score: float) -> float:
        """Score this rule against the current input."""
        score = self.base_weight
        normalized_mitre = mitre_technique.lower()
        normalized_activities = " ".join(previous_activities).lower()

        if any(pattern.lower() in normalized_mitre for pattern in self.mitre_patterns):
            score += 0.24
        if any(pattern.lower() in normalized_activities for pattern in self.activity_patterns):
            score += 0.18
        score += min(max(anomaly_score, 0.0), 1.0) * 0.18
        return score


class AttackPredictionRuleEngine:
    """Evaluate attack-chain rules."""

    def __init__(self):
        self.rules = (
            AttackRule(
                name="Valid account abuse to discovery",
                current_stage="initial_access",
                next_attack="Internal discovery using valid accounts",
                next_stage="discovery",
                mitre_patterns=("T1078", "valid account"),
                activity_patterns=("impossible travel", "new device", "unusual login", "vpn"),
                base_weight=0.48,
                defense="Revoke suspicious sessions, enforce MFA challenge, and monitor account enumeration.",
            ),
            AttackRule(
                name="Script execution to persistence",
                current_stage="execution",
                next_attack="Persistence through scheduled task or startup execution",
                next_stage="persistence",
                mitre_patterns=("T1059", "powershell", "command"),
                activity_patterns=("powershell", "encoded command", "script", "rundll32", "wscript"),
                base_weight=0.52,
                defense="Restrict script interpreters, inspect scheduled tasks, and isolate endpoints with suspicious process trees.",
            ),
            AttackRule(
                name="Credential access to lateral movement",
                current_stage="credential_access",
                next_attack="Lateral movement using stolen credentials",
                next_stage="lateral_movement",
                mitre_patterns=("T1003", "credential", "lsass", "dump"),
                activity_patterns=("failed login", "password spray", "credential dump", "lsass"),
                base_weight=0.58,
                defense="Reset credentials, revoke tokens, restrict remote admin protocols, and inspect privileged logons.",
            ),
            AttackRule(
                name="Discovery to collection",
                current_stage="discovery",
                next_attack="Sensitive data collection and staging",
                next_stage="collection",
                mitre_patterns=("T1083", "file discovery", "T1087", "account discovery"),
                activity_patterns=("share enumeration", "directory listing", "file access", "database listing"),
                base_weight=0.46,
                defense="Monitor bulk access, restrict sensitive shares, and investigate archive or staging activity.",
            ),
            AttackRule(
                name="Collection to exfiltration",
                current_stage="collection",
                next_attack="Data exfiltration over external channel",
                next_stage="exfiltration",
                mitre_patterns=("T1560", "archive", "collection"),
                activity_patterns=("archive", "zip", "large download", "staging", "bulk access"),
                base_weight=0.62,
                defense="Block suspicious egress, throttle large transfers, and preserve data access evidence.",
            ),
            AttackRule(
                name="Command and control to impact",
                current_stage="command_and_control",
                next_attack="Impact action such as encryption or destructive operation",
                next_stage="impact",
                mitre_patterns=("T1071", "application layer protocol", "command and control"),
                activity_patterns=("beacon", "callback", "c2", "payload", "ransomware"),
                base_weight=0.54,
                defense="Block command channels, isolate affected hosts, and prepare backup-based recovery.",
            ),
        )

    def evaluate(self, *, current_stage: str, mitre_technique: str, previous_activities: list[str], anomaly_score: float):
        """Return scored rule candidates for the current stage."""
        candidates = []
        for rule in self.rules:
            stage_match = rule.current_stage == current_stage
            score = rule.score(
                mitre_technique=mitre_technique,
                previous_activities=previous_activities,
                anomaly_score=anomaly_score,
            )
            if stage_match:
                score += 0.22
            candidates.append((rule, score))
        return sorted(candidates, key=lambda item: item[1], reverse=True)
