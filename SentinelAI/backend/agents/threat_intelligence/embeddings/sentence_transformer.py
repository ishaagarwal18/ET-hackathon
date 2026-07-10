"""Sentence Transformer embedding adapter."""

from agents.threat_intelligence.constants import DEFAULT_EMBEDDING_MODEL


class SentenceTransformerEmbedder:
    """Generate embeddings with sentence-transformers."""

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("sentence-transformers is required for Threat Intelligence embeddings.") from exc

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]):
        """Embed document texts."""
        return self.model.encode(texts, normalize_embeddings=True).astype("float32")

    def embed_query(self, text: str):
        """Embed one query."""
        return self.model.encode([text], normalize_embeddings=True).astype("float32")
