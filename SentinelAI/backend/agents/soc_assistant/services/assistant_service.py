"""AI SOC Assistant service built on the existing RAG pipeline."""

import json
from textwrap import shorten

from agents.soc_assistant.repositories.history_repository import SOCAssistantHistoryRepository
from agents.threat_intelligence.services.chat_service import ThreatIntelligenceChatService


class SOCAssistantService:
    """SOC analyst assistant for alerts, CVEs, mitigations, intelligence, and incidents."""

    def __init__(self, rag_service=None, history_repository=None):
        self.rag_service = rag_service or ThreatIntelligenceChatService()
        self.history_repository = history_repository or SOCAssistantHistoryRepository()

    def chat(self, *, tenant_id: str, user_id: str, message: str, context: dict | None = None) -> dict:
        """Generate one SOC Assistant response."""
        context = context or {}
        intent = self.detect_intent(message, context)
        rag_question = self.build_rag_question(intent=intent, message=message, context=context)
        rag_response = self.rag_service.chat(
            tenant_id=tenant_id,
            user_id=user_id,
            question=rag_question,
            top_k=5,
        )
        response = self.compose_response(intent=intent, message=message, context=context, rag_response=rag_response)
        conversation_id = self.history_repository.save_turn(
            tenant_id=tenant_id,
            user_id=user_id,
            message=message,
            response=response,
        )
        return {"conversation_id": conversation_id, **response}

    def history(self, *, tenant_id: str, user_id: str, limit: int = 25, offset: int = 0) -> list[dict]:
        """Return assistant conversation history."""
        return self.history_repository.list_history(
            tenant_id=tenant_id,
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

    def stream_events(self, *, response: dict):
        """Yield server-sent events for a completed assistant response."""
        yield self.event("metadata", {"intent": response["intent"], "conversation_id": response.get("conversation_id")})
        words = response["answer"].split()
        buffer = []
        for word in words:
            buffer.append(word)
            if len(buffer) >= 8:
                yield self.event("token", {"text": " ".join(buffer) + " "})
                buffer = []
        if buffer:
            yield self.event("token", {"text": " ".join(buffer)})
        yield self.event("citations", response.get("citations", []))
        yield self.event("done", {"success": True})

    def detect_intent(self, message: str, context: dict) -> str:
        """Classify analyst intent with transparent keyword rules."""
        text = f"{message} {json.dumps(context, default=str)}".lower()
        if "cve" in text or "cvss" in text or "vulnerability" in text:
            return "explain_cve"
        if "mitigation" in text or "recommend" in text or "remediate" in text:
            return "recommend_mitigation"
        if "incident" in text or "summarize" in text or "timeline" in text:
            return "summarize_incident"
        if "threat intel" in text or "ioc" in text or "mitre" in text or "ttp" in text:
            return "search_threat_intelligence"
        return "explain_alert"

    def build_rag_question(self, *, intent: str, message: str, context: dict) -> str:
        """Build a retrieval-focused question for the existing RAG pipeline."""
        context_text = json.dumps(context, indent=2, default=str)[:2500]
        instructions = {
            "explain_alert": "Explain this SOC alert, likely cause, related MITRE techniques, and analyst triage steps.",
            "explain_cve": "Explain this CVE or vulnerability, exploitation risk, affected assets, and prioritization guidance.",
            "recommend_mitigation": "Recommend practical mitigations, compensating controls, and validation steps.",
            "search_threat_intelligence": "Search threat intelligence context, summarize relevant IOCs, CVEs, advisories, and ATT&CK techniques.",
            "summarize_incident": "Summarize this incident, timeline, impact, MITRE mapping, response actions, and next steps.",
        }
        return f"{instructions[intent]}\n\nAnalyst question: {message}\n\nContext:\n{context_text}"

    def compose_response(self, *, intent: str, message: str, context: dict, rag_response: dict) -> dict:
        """Compose a professional SOC response."""
        title = {
            "explain_alert": "Alert Explanation",
            "explain_cve": "CVE Explanation",
            "recommend_mitigation": "Mitigation Recommendation",
            "search_threat_intelligence": "Threat Intelligence Search",
            "summarize_incident": "Incident Summary",
        }[intent]
        answer = (
            f"{title}\n\n"
            f"{rag_response.get('answer', 'No RAG response was available.')}\n\n"
            f"Analyst Focus\n"
            f"- Question: {shorten(message, width=240, placeholder='...')}\n"
            f"- Priority: validate evidence, scope affected assets, and document response actions.\n"
            f"- Confidence depends on available telemetry and cited intelligence."
        )
        recommendations = self.recommendations_for_intent(intent)
        return {
            "intent": intent,
            "answer": answer,
            "citations": rag_response.get("citations", []),
            "attack_techniques": rag_response.get("attack_techniques", []),
            "recommendations": recommendations,
            "context_summary": {
                "provided_fields": sorted(context.keys()),
                "context_available": bool(context),
            },
        }

    def recommendations_for_intent(self, intent: str) -> list[str]:
        """Return baseline SOC recommendations for an intent."""
        recommendations = {
            "explain_alert": [
                "Correlate the alert with recent logs, user activity, and affected assets.",
                "Check whether the behavior matches a known ATT&CK technique.",
                "Escalate if the signal repeats or touches critical assets.",
            ],
            "explain_cve": [
                "Validate exposure and asset criticality before assigning remediation priority.",
                "Check exploit maturity, compensating controls, and patch availability.",
                "Monitor for exploitation attempts until remediation is complete.",
            ],
            "recommend_mitigation": [
                "Apply least-disruptive containment first unless impact is confirmed.",
                "Preserve evidence before destructive remediation.",
                "Verify mitigation effectiveness with telemetry and follow-up scans.",
            ],
            "search_threat_intelligence": [
                "Pivot on IOCs across logs, alerts, and endpoint telemetry.",
                "Map findings to MITRE tactics and techniques.",
                "Track source confidence and citation provenance.",
            ],
            "summarize_incident": [
                "Confirm timeline accuracy with source telemetry.",
                "Separate observed facts from inferred attacker intent.",
                "Document containment, eradication, and recovery decisions.",
            ],
        }
        return recommendations[intent]

    def event(self, event_type: str, payload) -> str:
        """Format a server-sent event."""
        return f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"
