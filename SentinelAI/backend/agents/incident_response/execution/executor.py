"""Playbook execution for simulated incident response."""

from dataclasses import asdict
from datetime import UTC, datetime

from agents.incident_response.actions.simulated_actions import ACTION_REGISTRY


class PlaybookExecutor:
    """Execute playbook steps in simulation mode."""

    def execute(self, *, playbook, incident: dict, approval_decision) -> list[dict]:
        """Run permitted playbook steps and return execution logs."""
        execution_logs = []
        for step in playbook.steps:
            target = incident.get(step.target_field)
            if not target:
                execution_logs.append(
                    {
                        "action": step.action,
                        "target": None,
                        "status": "skipped",
                        "simulated": True,
                        "message": f"Missing required incident field '{step.target_field}'.",
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                )
                continue

            if step.requires_approval and approval_decision.status != "approved":
                execution_logs.append(
                    {
                        "action": step.action,
                        "target": target,
                        "status": "approval_required",
                        "simulated": True,
                        "message": "Action was not executed because approval is pending.",
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                )
                continue

            action = ACTION_REGISTRY[step.action]
            result = action.execute(target=target, context=incident)
            execution_logs.append(asdict(result))

        return execution_logs
