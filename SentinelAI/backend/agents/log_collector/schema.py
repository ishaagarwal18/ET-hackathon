"""Normalized log schema for SentinelAI."""

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class NormalizedLog:
    """Canonical log document stored by the Log Collector Agent."""

    tenant_id: str
    source_type: str
    source_name: str
    event_type: str
    severity: str
    message: str
    observed_at: datetime
    event_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "new"
    hostname: str | None = None
    ip_address: str | None = None
    username: str | None = None
    process_name: str | None = None
    action: str | None = None
    outcome: str | None = None
    asset_id: str | None = None
    user_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)
    normalized: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None

    def to_document(self) -> dict[str, Any]:
        """Return MongoDB-ready document."""
        document = asdict(self)
        document["correlation"] = {
            "trace_id": self.metadata.get("trace_id"),
            "session_id": self.metadata.get("session_id"),
            "parent_event_id": self.metadata.get("parent_event_id"),
        }
        return document
