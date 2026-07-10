"""MongoDB repository for behavior profiles."""

from datetime import UTC, datetime

from ai_engines.behavioral_anomaly.constants import BEHAVIOR_PROFILE_COLLECTION
from core.mongodb import get_mongo_database


class BehaviorProfileRepository:
    """Persist behavior profile analysis results."""

    def __init__(self):
        self.collection = get_mongo_database()[BEHAVIOR_PROFILE_COLLECTION]

    def upsert_profile(self, *, tenant_id: str, user_identifier: str, profile: dict) -> str:
        """Create or update a user's behavior profile."""
        now = datetime.now(UTC)
        document = {
            **profile,
            "tenant_id": tenant_id,
            "profile_key": f"{tenant_id}:{user_identifier}",
            "subject_type": "user",
            "status": "active",
            "updated_at": now,
            "metadata": {
                **profile.get("metadata", {}),
                "engine": "isolation_forest",
                "future_sequence_model": "lstm_ready",
            },
        }

        result = self.collection.update_one(
            {"tenant_id": tenant_id, "profile_key": document["profile_key"]},
            {
                "$set": document,
                "$setOnInsert": {
                    "created_at": now,
                    "deleted_at": None,
                },
            },
            upsert=True,
        )
        return str(result.upserted_id) if result.upserted_id else document["profile_key"]
