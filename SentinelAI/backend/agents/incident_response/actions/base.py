"""Base action contracts for simulated response actions."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ActionResult:
    """Execution result for a simulated response action."""

    action_id: str
    action: str
    target: str
    status: str
    simulated: bool
    message: str
    timestamp: str


class SimulatedResponseAction:
    """Base class for response actions that never touch real infrastructure."""

    action_name: str

    def execute(self, target: str, context: dict | None = None) -> ActionResult:
        """Simulate action execution and return an audit-friendly result."""
        return ActionResult(
            action_id=str(uuid4()),
            action=self.action_name,
            target=target,
            status="simulated_success",
            simulated=True,
            message=self.build_message(target=target, context=context or {}),
            timestamp=datetime.now(UTC).isoformat(),
        )

    def build_message(self, *, target: str, context: dict) -> str:
        """Return action-specific execution message."""
        return f"Simulated {self.action_name} for target {target}."
