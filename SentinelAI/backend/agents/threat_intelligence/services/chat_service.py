"""Threat Intelligence Agent chat service."""

from agents.threat_intelligence.qa.answerer import ThreatIntelAnswerer
from agents.threat_intelligence.repositories.chat_history import ThreatIntelChatHistoryRepository
from agents.threat_intelligence.retrievers.faiss_retriever import ThreatIntelRetriever


class ThreatIntelligenceChatService:
    """Coordinate retrieval, answer generation, citations, and history."""

    def __init__(self, retriever=None, answerer=None, history_repository=None):
        self.retriever = retriever or ThreatIntelRetriever()
        self.answerer = answerer or ThreatIntelAnswerer()
        self.history_repository = history_repository or ThreatIntelChatHistoryRepository()

    def chat(self, *, tenant_id: str, user_id: str, question: str, top_k: int = 5) -> dict:
        """Answer a threat intelligence question."""
        retrieved = self.retriever.retrieve(question, top_k=top_k)
        response = self.answerer.answer(question, retrieved)
        chat_id = self.history_repository.save_message(
            tenant_id=tenant_id,
            user_id=user_id,
            question=question,
            response=response,
        )
        return {
            "chat_id": chat_id,
            "question": question,
            **response,
        }

    def history(self, *, tenant_id: str, user_id: str, limit: int = 25, offset: int = 0) -> list[dict]:
        """Return prior chat exchanges."""
        return self.history_repository.list_history(
            tenant_id=tenant_id,
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
