"""Base parser contracts and helpers."""

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from agents.log_collector.constants import SEVERITY_MAP
from agents.log_collector.schema import NormalizedLog


class BaseLogParser(ABC):
    """Base class for log source parsers."""

    source_type: str

    def __init__(self, tenant_id: str, source_name: str | None = None):
        self.tenant_id = tenant_id
        self.source_name = source_name or self.source_type

    @abstractmethod
    def parse(self, content: str) -> list[NormalizedLog]:
        """Parse source content into normalized logs."""

    def normalize_severity(self, value: Any) -> str:
        """Normalize severity values to SentinelAI severity levels."""
        if value is None:
            return "informational"
        return SEVERITY_MAP.get(str(value).strip().lower(), "informational")

    def parse_datetime(self, value: Any) -> datetime:
        """Parse common timestamp formats into timezone-aware datetimes."""
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=UTC)
        if not value:
            return datetime.now(UTC)

        text = str(value).strip()
        formats = (
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%b %d %H:%M:%S",
            "%m/%d/%Y %I:%M:%S %p",
        )
        for fmt in formats:
            try:
                parsed = datetime.strptime(text, fmt)
                if fmt == "%b %d %H:%M:%S":
                    parsed = parsed.replace(year=datetime.now(UTC).year)
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
            except ValueError:
                continue
        return datetime.now(UTC)

    def build_log(
        self,
        *,
        event_type: str,
        severity: Any,
        message: str,
        observed_at: Any = None,
        raw: dict[str, Any] | None = None,
        **kwargs,
    ) -> NormalizedLog:
        """Create a normalized log object."""
        return NormalizedLog(
            tenant_id=self.tenant_id,
            source_type=self.source_type,
            source_name=self.source_name,
            event_type=event_type or "unknown",
            severity=self.normalize_severity(severity),
            message=message or "",
            observed_at=self.parse_datetime(observed_at),
            raw=raw or {},
            normalized=kwargs.pop("normalized", {}),
            metadata=kwargs.pop("metadata", {}),
            **kwargs,
        )
