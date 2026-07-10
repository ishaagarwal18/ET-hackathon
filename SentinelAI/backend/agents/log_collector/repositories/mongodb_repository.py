"""MongoDB repository for normalized logs."""

from bson import ObjectId
from pymongo import DESCENDING

from agents.log_collector.constants import NORMALIZED_LOG_COLLECTION
from core.mongodb import get_mongo_database


class MongoLogRepository:
    """Persist and query normalized log documents."""

    def __init__(self):
        self.collection = get_mongo_database()[NORMALIZED_LOG_COLLECTION]

    def insert_many(self, documents: list[dict]) -> list[str]:
        """Insert normalized log documents and return inserted IDs."""
        if not documents:
            return []
        result = self.collection.insert_many(documents, ordered=False)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

    def list_logs(self, *, tenant_id: str, limit: int = 50, offset: int = 0, filters: dict | None = None) -> list[dict]:
        """List normalized logs by tenant with optional filters."""
        query = {"tenant_id": tenant_id, "deleted_at": None}
        if filters:
            query.update(filters)
        cursor = (
            self.collection.find(query)
            .sort("observed_at", DESCENDING)
            .skip(offset)
            .limit(min(limit, 500))
        )
        return [self.serialize_document(document) for document in cursor]

    def get_log(self, *, tenant_id: str, log_id: str) -> dict | None:
        """Return a normalized log by ID and tenant."""
        document = self.collection.find_one(
            {
                "_id": ObjectId(log_id),
                "tenant_id": tenant_id,
                "deleted_at": None,
            }
        )
        return self.serialize_document(document) if document else None

    def count_logs(self, *, tenant_id: str, filters: dict | None = None) -> int:
        """Count logs for pagination metadata."""
        query = {"tenant_id": tenant_id, "deleted_at": None}
        if filters:
            query.update(filters)
        return self.collection.count_documents(query)

    def serialize_document(self, document: dict) -> dict:
        """Convert MongoDB document values into API-safe primitives."""
        document["id"] = str(document.pop("_id"))
        for key in ("created_at", "updated_at", "deleted_at", "observed_at"):
            if document.get(key):
                document[key] = document[key].isoformat()
        return document
