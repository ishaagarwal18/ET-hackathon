"""Autonomous incident response service."""

from dataclasses import asdict
from uuid import uuid4

from agents.incident_response.approval.workflow import ApprovalWorkflow
from agents.incident_response.execution.executor import PlaybookExecutor
from agents.incident_response.playbooks.catalog import get_playbook


class AutonomousIncidentResponseService:
    """Plan and simulate incident response playbooks."""

    def __init__(self, approval_workflow=None, executor=None):
        self.approval_workflow = approval_workflow or ApprovalWorkflow()
        self.executor = executor or PlaybookExecutor()

    def respond(self, *, incident: dict, risk_level: str, approval: dict | None = None) -> dict:
        """Simulate playbook execution and return execution logs."""
        playbook = get_playbook(risk_level)
        approval_decision = self.approval_workflow.evaluate(risk_level=risk_level, approval=approval)
        execution_logs = self.executor.execute(
            playbook=playbook,
            incident=incident,
            approval_decision=approval_decision,
        )

        return {
            "response_id": str(uuid4()),
            "mode": "simulation",
            "risk_level": risk_level,
            "playbook": {
                "name": playbook.name,
                "objective": playbook.objective,
                "steps": [
                    {
                        "action": step.action,
                        "target_field": step.target_field,
                        "description": step.description,
                        "requires_approval": step.requires_approval,
                    }
                    for step in playbook.steps
                ],
            },
            "approval": asdict(approval_decision),
            "execution_logs": execution_logs,
            "summary": {
                "total_actions": len(execution_logs),
                "simulated_success": sum(1 for item in execution_logs if item["status"] == "simulated_success"),
                "approval_required": sum(1 for item in execution_logs if item["status"] == "approval_required"),
                "skipped": sum(1 for item in execution_logs if item["status"] == "skipped"),
            },
        }
