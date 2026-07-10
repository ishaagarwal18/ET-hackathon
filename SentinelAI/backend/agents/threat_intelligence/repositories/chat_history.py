"""MongoDB chat history repository."""

from datetime import UTC, datetime

from bson import ObjectId
from pymongo import DESCENDING

from agents.threat_intelligence.constants import CHAT_HISTORY_COLLECTION
from core.mongodb import get_mongo_database


class ThreatIntelChatHistoryRepository:
    """Persist and retrieve threat intelligence chat history."""

    def __init__(self):
        self.collection = get_mongo_database()[CHAT_HISTORY_COLLECTION]

    def save_message(self, *, tenant_id: str, user_id: str, question: str, response: dict) -> str:
        """Store one chat exchange."""
        now = datetime.now(UTC)
        document = {
            "tenant_id": tenant_id,
            "user_id": str(user_id),
            "question": question,
            "answer": response["answer"],
            "attack_techniques": response.get("attack_techniques", []),
            "citations": response.get("citations", []),
            "created_at": now,
            "updated_at": now,
            "status": "active",
            "metadata": {
                "agent": "threat_intelligence",
                "retriever": "faiss",
                "embeddings": "sentence_transformers",
            },
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def list_history(self, *, tenant_id: str, user_id: str, limit: int = 25, offset: int = 0) -> list[dict]:
        """Return recent chat history."""
        cursor = (
            self.collection.find({"tenant_id": tenant_id, "user_id": str(user_id), "status": "active"})
            .sort("created_at", DESCENDING)
            .skip(offset)
            .limit(min(limit, 100))
        )
        return [self.serialize(document) for document in cursor]

    def serialize(self, document: dict) -> dict:
        """Convert Mongo document to API-safe dict."""
        document["id"] = str(document.pop("_id", ObjectId()))
        for key in ("created_at", "updated_at"):
            if document.get(key):
                document[key] = document[key].isoformat()
        return document
