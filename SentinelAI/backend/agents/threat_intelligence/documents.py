"""Document contracts for the Threat Intelligence Agent."""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ThreatIntelDocument:
    """Canonical threat intelligence document chunk."""

    content: str
    source: str
    title: str
    citation: str
    document_id: str
    metadata: dict = field(default_factory=dict)
