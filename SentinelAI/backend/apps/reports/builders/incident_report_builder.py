"""Build normalized incident report documents."""

from datetime import UTC, datetime
from uuid import uuid4


class IncidentReportBuilder:
    """Create a complete incident report payload from validated input."""

    def build(self, *, tenant_id: str, requested_by: str, payload: dict) -> dict:
        """Return a complete report document ready for export."""
        generated_at = datetime.now(UTC)
        incident = payload["incident"]
        risk_score = payload["risk_score"]

        return {
            "report_id": str(uuid4()),
            "report_type": "incident",
            "tenant_id": tenant_id,
            "requested_by": requested_by,
            "generated_at": generated_at.isoformat(),
            "executive_summary": payload["executive_summary"],
            "incident": {
                "incident_id": incident["incident_id"],
                "title": incident["title"],
                "severity": incident["severity"],
                "status": incident["status"],
                "owner": incident.get("owner", "Unassigned"),
            },
            "risk_score": {
                "score": risk_score["score"],
                "level": risk_score["level"],
                "rationale": risk_score.get("rationale", ""),
            },
            "timeline": payload.get("timeline", []),
            "mitre_mapping": payload.get("mitre_mapping", []),
            "affected_assets": payload.get("affected_assets", []),
            "response_actions": payload.get("response_actions", []),
            "recommendations": payload.get("recommendations", []),
            "metadata": {
                "classification": payload.get("classification", "internal"),
                "generated_by": "SentinelAI Report Generator",
                "formats_supported": ["pdf", "csv", "json"],
            },
        }
