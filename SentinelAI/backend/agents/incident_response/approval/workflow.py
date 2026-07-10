"""Approval workflow for simulated incident response."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ApprovalDecision:
    """Approval decision for a playbook execution."""

    approval_id: str
    status: str
    approved_by: str | None
    reason: str
    timestamp: str


class ApprovalWorkflow:
    """Evaluate approval requirements for response playbooks."""

    def evaluate(self, *, risk_level: str, approval: dict | None) -> ApprovalDecision:
        """Return approved/pending decision for a requested playbook execution."""
        approval = approval or {}
        requires_approval = risk_level in {"medium", "critical"}
        approved = bool(approval.get("approved"))
        approved_by = approval.get("approved_by")

        if not requires_approval:
            return ApprovalDecision(
                approval_id=str(uuid4()),
                status="not_required",
                approved_by=None,
                reason="Low risk playbook does not require approval.",
                timestamp=datetime.now(UTC).isoformat(),
            )

        if approved and approved_by:
            return ApprovalDecision(
                approval_id=str(uuid4()),
                status="approved",
                approved_by=approved_by,
                reason=approval.get("reason", "Approved for simulated containment."),
                timestamp=datetime.now(UTC).isoformat(),
            )

        return ApprovalDecision(
            approval_id=str(uuid4()),
            status="pending",
            approved_by=None,
            reason="Approval required before disruptive simulated response actions can execute.",
            timestamp=datetime.now(UTC).isoformat(),
        )
