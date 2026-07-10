"""MongoDB history repository for SOC Assistant conversations."""

from datetime import UTC, datetime

from pymongo import DESCENDING

from agents.soc_assistant.constants import SOC_ASSISTANT_HISTORY_COLLECTION
from core.mongodb import get_mongo_database


class SOCAssistantHistoryRepository:
    """Persist SOC Assistant conversation turns."""

    def __init__(self):
        self.collection = get_mongo_database()[SOC_ASSISTANT_HISTORY_COLLECTION]

    def save_turn(self, *, tenant_id: str, user_id: str, message: str, response: dict) -> str:
        """Store one assistant conversation turn."""
        now = datetime.now(UTC)
        document = {
            "tenant_id": tenant_id,
            "user_id": str(user_id),
            "message": message,
            "intent": response.get("intent"),
            "answer": response.get("answer"),
            "citations": response.get("citations", []),
            "recommendations": response.get("recommendations", []),
            "created_at": now,
            "updated_at": now,
            "status": "active",
            "metadata": {
                "assistant": "soc_assistant",
                "rag_pipeline": "threat_intelligence",
            },
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def list_history(self, *, tenant_id: str, user_id: str, limit: int = 25, offset: int = 0) -> list[dict]:
        """Return recent SOC Assistant conversation turns."""
        cursor = (
            self.collection.find({"tenant_id": tenant_id, "user_id": str(user_id), "status": "active"})
            .sort("created_at", DESCENDING)
            .skip(offset)
            .limit(min(limit, 100))
        )
        return [self.serialize(document) for document in cursor]

    def serialize(self, document: dict) -> dict:
        """Convert Mongo document to API-safe dict."""
        document["id"] = str(document.pop("_id"))
        for key in ("created_at", "updated_at"):
            if document.get(key):
                document[key] = document[key].isoformat()
        return document
