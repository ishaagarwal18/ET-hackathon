"""Apply SentinelAI MongoDB validators and indexes."""

from django.core.management.base import BaseCommand

from core.mongodb import get_mongo_database
from database.mongodb.apply import apply_mongodb_models


class Command(BaseCommand):
    """Create or update MongoDB collections, validators, and indexes."""

    help = "Apply SentinelAI MongoDB collection validators and indexes."

    def handle(self, *args, **options):
        database = get_mongo_database()
        applied = apply_mongodb_models(database)

        for collection_name in applied:
            self.stdout.write(self.style.SUCCESS(f"Applied MongoDB model: {collection_name}"))
