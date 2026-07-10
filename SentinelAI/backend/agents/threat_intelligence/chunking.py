"""Document chunking utilities."""

from uuid import NAMESPACE_URL, uuid5

from agents.threat_intelligence.documents import ThreatIntelDocument
from agents.threat_intelligence.langchain_adapter import from_langchain_document, to_langchain_document


def chunk_document(document: ThreatIntelDocument, chunk_size: int = 900, overlap: int = 120) -> list[ThreatIntelDocument]:
    """Split a document into overlapping retrieval chunks."""
    content = " ".join(document.content.split())
    if len(content) <= chunk_size:
        return [document]

    chunks = []
    start = 0
    index = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        text = content[start:end]
        chunk_id = str(uuid5(NAMESPACE_URL, f"{document.document_id}:{index}"))
        chunks.append(
            ThreatIntelDocument(
                content=text,
                source=document.source,
                title=document.title,
                citation=document.citation,
                document_id=chunk_id,
                metadata={**document.metadata, "parent_document_id": document.document_id, "chunk_index": index},
            )
        )
        if end == len(content):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks


def chunk_documents(documents: list[ThreatIntelDocument]) -> list[ThreatIntelDocument]:
    """Chunk many documents."""
    chunks = []
    for document in documents:
        chunks.extend(chunk_document(document))
    # Round-trip through LangChain's Document contract so the retrieval layer can
    # evolve toward LangChain-native loaders, splitters, and chains cleanly.
    return [from_langchain_document(to_langchain_document(chunk)) for chunk in chunks]
