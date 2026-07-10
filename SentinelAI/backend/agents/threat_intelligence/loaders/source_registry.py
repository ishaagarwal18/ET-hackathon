"""Knowledge source registry."""

from pathlib import Path

from agents.threat_intelligence.constants import SAMPLE_KNOWLEDGE_DIR, SUPPORTED_KNOWLEDGE_SOURCES
from agents.threat_intelligence.loaders.local_loader import LocalThreatIntelLoader


def get_default_loaders(base_dir: Path = SAMPLE_KNOWLEDGE_DIR):
    """Return configured loaders for MITRE, CERT-In, CVE, and NVD knowledge."""
    return [
        LocalThreatIntelLoader(source_name=source, directory=base_dir / source)
        for source in SUPPORTED_KNOWLEDGE_SOURCES
    ]
