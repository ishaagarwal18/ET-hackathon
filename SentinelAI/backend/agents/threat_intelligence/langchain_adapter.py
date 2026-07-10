"""LangChain integration helpers for Threat Intelligence Agent."""

from agents.threat_intelligence.documents import ThreatIntelDocument


def to_langchain_document(document: ThreatIntelDocument):
    """Convert SentinelAI document chunks to LangChain Document objects."""
    try:
        from langchain_core.documents import Document
    except ImportError as exc:
        raise RuntimeError("langchain is required for Threat Intelligence document orchestration.") from exc

    return Document(
        page_content=document.content,
        metadata={
            "source": document.source,
            "title": document.title,
            "citation": document.citation,
            "document_id": document.document_id,
            **document.metadata,
        },
    )


def from_langchain_document(document) -> ThreatIntelDocument:
    """Convert a LangChain Document back to SentinelAI's document contract."""
    metadata = dict(document.metadata or {})
    return ThreatIntelDocument(
        content=document.page_content,
        source=metadata.pop("source", "unknown"),
        title=metadata.pop("title", "Untitled"),
        citation=metadata.pop("citation", "unknown"),
        document_id=metadata.pop("document_id", "unknown"),
        metadata=metadata,
    )


def build_threat_intel_prompt(question: str, context: str) -> str:
    """Build the QA prompt through LangChain prompt templates."""
    try:
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as exc:
        raise RuntimeError("langchain is required for Threat Intelligence question answering.") from exc

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are SentinelAI's Threat Intelligence Agent. Answer only from the supplied context, "
                "explain attack techniques clearly, and preserve citations.",
            ),
            (
                "human",
                "Question: {question}\n\nRetrieved context:\n{context}\n\nReturn a grounded analyst answer.",
            ),
        ]
    )
    return prompt.format(question=question, context=context)
