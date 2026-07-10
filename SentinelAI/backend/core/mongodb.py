"""MongoDB client utilities for SentinelAI."""

from functools import lru_cache
from typing import TYPE_CHECKING, Any

from django.conf import settings

if TYPE_CHECKING:
    from pymongo import MongoClient
    from pymongo.database import Database


@lru_cache(maxsize=1)
def get_mongo_client() -> "MongoClient[Any]":
    """Return a cached MongoDB client configured from Django settings."""
    from pymongo import MongoClient

    return MongoClient(
        settings.MONGODB["URI"],
        connectTimeoutMS=settings.MONGODB["CONNECT_TIMEOUT_MS"],
        serverSelectionTimeoutMS=settings.MONGODB["SERVER_SELECTION_TIMEOUT_MS"],
    )


def get_mongo_database() -> "Database[Any]":
    """Return the configured SentinelAI MongoDB database."""
    return get_mongo_client()[settings.MONGODB["NAME"]]


def check_mongodb_connection() -> bool:
    """Return True when MongoDB responds to a ping command."""
    get_mongo_client().admin.command("ping")
    return True
