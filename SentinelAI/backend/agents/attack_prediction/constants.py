"""Constants for the AI Attack Prediction Agent."""

ATTACK_STAGES = (
    "reconnaissance",
    "initial_access",
    "execution",
    "persistence",
    "privilege_escalation",
    "defense_evasion",
    "credential_access",
    "discovery",
    "lateral_movement",
    "collection",
    "command_and_control",
    "exfiltration",
    "impact",
)

STAGE_ORDER = {stage: index for index, stage in enumerate(ATTACK_STAGES)}

DEFAULT_DEFENSES = {
    "reconnaissance": "Harden public exposure, monitor scanning, and validate external attack surface inventory.",
    "initial_access": "Enforce MFA, block malicious infrastructure, patch exposed systems, and inspect phishing indicators.",
    "execution": "Restrict script interpreters, alert on suspicious process trees, and quarantine affected endpoints.",
    "persistence": "Audit autoruns, scheduled tasks, services, startup folders, and identity persistence mechanisms.",
    "privilege_escalation": "Review privilege changes, constrain admin groups, and investigate exploit or token abuse.",
    "defense_evasion": "Validate security tooling health, block tampering attempts, and restore telemetry coverage.",
    "credential_access": "Reset exposed credentials, revoke sessions, monitor secrets access, and enforce phishing-resistant MFA.",
    "discovery": "Alert on abnormal enumeration of users, shares, groups, processes, cloud resources, and network topology.",
    "lateral_movement": "Segment networks, disable suspicious remote sessions, restrict admin protocols, and isolate endpoints.",
    "collection": "Monitor bulk file access, sensitive repository access, archive creation, and staging directories.",
    "command_and_control": "Block suspicious egress, inspect beaconing, sinkhole malicious domains, and capture network evidence.",
    "exfiltration": "Throttle and inspect outbound transfers, block unsanctioned destinations, and preserve data access logs.",
    "impact": "Activate incident response, isolate affected systems, protect backups, and prepare recovery workflows.",
}
