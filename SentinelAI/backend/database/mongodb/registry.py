"""MongoDB schema registry helpers."""

from database.mongodb.collections import COLLECTIONS
from database.mongodb.indexes import COLLECTION_INDEXES
from database.mongodb.schemas import COLLECTION_SCHEMAS


def get_collection_model(collection_name: str) -> dict:
    """Return validator and index definitions for a collection."""
    if collection_name not in COLLECTION_SCHEMAS:
        raise KeyError(f"Unknown MongoDB collection: {collection_name}")

    return {
        "name": collection_name,
        "validator": COLLECTION_SCHEMAS[collection_name],
        "indexes": COLLECTION_INDEXES.get(collection_name, []),
    }


def iter_collection_models():
    """Yield all registered MongoDB collection models."""
    for collection_name in COLLECTIONS.values():
        yield get_collection_model(collection_name)
