"""FAISS vector store adapter."""

import pickle
from pathlib import Path

from agents.threat_intelligence.constants import VECTOR_INDEX_DIR


class FAISSThreatIntelStore:
    """Persist and query threat intelligence vectors with FAISS."""

    def __init__(self, index_dir: Path = VECTOR_INDEX_DIR):
        try:
            import faiss
        except ImportError as exc:
            raise RuntimeError("faiss-cpu is required for Threat Intelligence vector search.") from exc

        self.faiss = faiss
        self.index_dir = index_dir
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.index_dir / "index.faiss"
        self.metadata_path = self.index_dir / "documents.pkl"
        self.index = None
        self.documents = []

    def build(self, embeddings, documents) -> None:
        """Build and persist a FAISS index."""
        dimension = embeddings.shape[1]
        self.index = self.faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.documents = documents
        self.faiss.write_index(self.index, str(self.index_path))
        with self.metadata_path.open("wb") as handle:
            pickle.dump(self.documents, handle)

    def load(self) -> bool:
        """Load an existing FAISS index if present."""
        if not self.index_path.exists() or not self.metadata_path.exists():
            return False
        self.index = self.faiss.read_index(str(self.index_path))
        with self.metadata_path.open("rb") as handle:
            self.documents = pickle.load(handle)
        return True

    def search(self, query_embedding, top_k: int = 5):
        """Search for nearest document chunks."""
        if self.index is None:
            raise RuntimeError("FAISS index is not loaded.")
        scores, indexes = self.index.search(query_embedding, top_k)
        results = []
        for score, index in zip(scores[0], indexes[0]):
            if index == -1:
                continue
            document = self.documents[index]
            results.append({"score": float(score), "document": document})
        return results
