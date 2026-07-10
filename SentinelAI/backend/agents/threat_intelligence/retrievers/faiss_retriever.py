"""FAISS-backed retriever."""

from agents.threat_intelligence.chunking import chunk_documents
from agents.threat_intelligence.embeddings.sentence_transformer import SentenceTransformerEmbedder
from agents.threat_intelligence.loaders.source_registry import get_default_loaders
from agents.threat_intelligence.vectorstores.faiss_store import FAISSThreatIntelStore


class ThreatIntelRetriever:
    """Retrieve relevant threat intelligence chunks."""

    def __init__(self, embedder=None, vector_store=None, loaders=None):
        self.embedder = embedder or SentenceTransformerEmbedder()
        self.vector_store = vector_store or FAISSThreatIntelStore()
        self.loaders = loaders or get_default_loaders()

    def ensure_ready(self) -> None:
        """Load or build the vector index."""
        if self.vector_store.load():
            return

        documents = []
        for loader in self.loaders:
            documents.extend(loader.load())
        chunks = chunk_documents(documents)
        embeddings = self.embedder.embed_documents([chunk.content for chunk in chunks])
        self.vector_store.build(embeddings, chunks)

    def retrieve(self, question: str, top_k: int = 5):
        """Retrieve relevant source chunks."""
        self.ensure_ready()
        query_embedding = self.embedder.embed_query(question)
        return self.vector_store.search(query_embedding, top_k=top_k)
