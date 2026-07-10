"""Risk-based incident response playbook catalog."""

from dataclasses import dataclass

from agents.incident_response.constants import (
    ACTION_BLOCK_IP,
    ACTION_DISABLE_USER,
    ACTION_DISCONNECT_DEVICE,
    ACTION_KILL_PROCESS,
    ACTION_SNAPSHOT_VM,
)


@dataclass(frozen=True, slots=True)
class PlaybookStep:
    """One playbook action step."""

    action: str
    target_field: str
    description: str
    requires_approval: bool = False


@dataclass(frozen=True, slots=True)
class ResponsePlaybook:
    """Incident response playbook definition."""

    risk_level: str
    name: str
    objective: str
    steps: tuple[PlaybookStep, ...]


PLAYBOOKS = {
    "low": ResponsePlaybook(
        risk_level="low",
        name="Low Risk Monitoring Playbook",
        objective="Contain obvious indicators while preserving normal business operations.",
        steps=(
            PlaybookStep(ACTION_BLOCK_IP, "ip", "Simulate temporary network block for the suspicious source IP."),
        ),
    ),
    "medium": ResponsePlaybook(
        risk_level="medium",
        name="Medium Risk Containment Playbook",
        objective="Contain active endpoint or user activity with analyst approval for disruptive actions.",
        steps=(
            PlaybookStep(ACTION_BLOCK_IP, "ip", "Simulate blocking the suspicious source IP."),
            PlaybookStep(ACTION_KILL_PROCESS, "process_name", "Simulate terminating the suspicious process."),
            PlaybookStep(ACTION_DISABLE_USER, "user_id", "Simulate disabling the suspected user account.", True),
        ),
    ),
    "critical": ResponsePlaybook(
        risk_level="critical",
        name="Critical Risk Isolation Playbook",
        objective="Rapidly contain high-confidence compromise while preserving forensic evidence.",
        steps=(
            PlaybookStep(ACTION_BLOCK_IP, "ip", "Simulate blocking command-and-control or attacker IP."),
            PlaybookStep(ACTION_KILL_PROCESS, "process_name", "Simulate terminating malicious process execution."),
            PlaybookStep(ACTION_DISABLE_USER, "user_id", "Simulate disabling compromised identity.", True),
            PlaybookStep(ACTION_DISCONNECT_DEVICE, "device_id", "Simulate isolating affected device.", True),
            PlaybookStep(ACTION_SNAPSHOT_VM, "vm_id", "Simulate VM snapshot for forensic preservation.", True),
        ),
    ),
}


def get_playbook(risk_level: str) -> ResponsePlaybook:
    """Return a playbook by risk level."""
    return PLAYBOOKS[risk_level]
