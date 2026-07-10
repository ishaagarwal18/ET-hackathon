"""Utilities for applying MongoDB collection validators and indexes."""

from pymongo.database import Database
from pymongo.errors import CollectionInvalid

from database.mongodb.registry import iter_collection_models


def apply_mongodb_models(database: Database) -> list[str]:
    """Create or update MongoDB collections, validators, and indexes."""
    applied = []
    existing_collections = set(database.list_collection_names())

    for model in iter_collection_models():
        collection_name = model["name"]
        validator = model["validator"]

        if collection_name not in existing_collections:
            try:
                database.create_collection(collection_name, validator=validator)
            except CollectionInvalid:
                pass
        else:
            database.command(
                {
                    "collMod": collection_name,
                    "validator": validator,
                    "validationLevel": "strict",
                    "validationAction": "error",
                }
            )

        database[collection_name].create_indexes(model["indexes"])
        applied.append(collection_name)

    return applied
