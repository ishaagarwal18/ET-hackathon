"""Document loader contracts."""

from abc import ABC, abstractmethod

from agents.threat_intelligence.documents import ThreatIntelDocument


class BaseThreatIntelLoader(ABC):
    """Base class for threat intelligence document loaders."""

    source_name: str

    @abstractmethod
    def load(self) -> list[ThreatIntelDocument]:
        """Load source documents."""
