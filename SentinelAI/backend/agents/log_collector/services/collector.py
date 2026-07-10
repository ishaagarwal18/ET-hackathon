"""Log Collector Agent application service."""

from agents.log_collector.parsers.factory import get_parser
from agents.log_collector.repositories.mongodb_repository import MongoLogRepository


class LogCollectorService:
    """Coordinate parsing, normalization, and persistence of logs."""

    def __init__(self, repository: MongoLogRepository | None = None):
        self.repository = repository or MongoLogRepository()

    def ingest(self, *, tenant_id: str, source_type: str, content: str, source_name: str | None = None) -> dict:
        """Normalize source log content and persist documents."""
        parser = get_parser(source_type=source_type, tenant_id=tenant_id, source_name=source_name)
        normalized_logs = parser.parse(content)
        documents = [log.to_document() for log in normalized_logs]
        inserted_ids = self.repository.insert_many(documents)
        return {
            "source_type": source_type,
            "source_name": source_name or source_type,
            "received": len(normalized_logs),
            "stored": len(inserted_ids),
            "log_ids": inserted_ids,
        }

    def list_logs(self, *, tenant_id: str, limit: int, offset: int, filters: dict | None = None) -> dict:
        """Return normalized logs with pagination metadata."""
        logs = self.repository.list_logs(tenant_id=tenant_id, limit=limit, offset=offset, filters=filters)
        total = self.repository.count_logs(tenant_id=tenant_id, filters=filters)
        return {
            "items": logs,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
            },
        }

    def get_log_details(self, *, tenant_id: str, log_id: str) -> dict | None:
        """Return a normalized log details document."""
        return self.repository.get_log(tenant_id=tenant_id, log_id=log_id)
