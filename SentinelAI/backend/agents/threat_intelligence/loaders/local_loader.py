"""Local file document loader for seed threat intelligence knowledge."""

from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

from agents.threat_intelligence.documents import ThreatIntelDocument
from agents.threat_intelligence.loaders.base import BaseThreatIntelLoader


class LocalThreatIntelLoader(BaseThreatIntelLoader):
    """Load local Markdown/TXT seed documents."""

    def __init__(self, source_name: str, directory: Path):
        self.source_name = source_name
        self.directory = directory

    def load(self) -> list[ThreatIntelDocument]:
        documents = []
        for path in sorted(self.directory.glob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            content = path.read_text(encoding="utf-8")
            document_id = str(uuid5(NAMESPACE_URL, f"{self.source_name}:{path.name}"))
            title = path.stem.replace("_", " ").title()
            documents.append(
                ThreatIntelDocument(
                    content=content,
                    source=self.source_name,
                    title=title,
                    citation=f"{self.source_name}:{path.name}",
                    document_id=document_id,
                    metadata={"path": str(path), "loader": "local_file"},
                )
            )
        return documents
