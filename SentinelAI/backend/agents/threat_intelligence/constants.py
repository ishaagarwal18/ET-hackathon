"""Constants for the Threat Intelligence Agent."""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
SAMPLE_KNOWLEDGE_DIR = BASE_DIR / "samples" / "threat_intelligence"
VECTOR_INDEX_DIR = BASE_DIR / "runtime" / "faiss" / "threat_intelligence"

CHAT_HISTORY_COLLECTION = "threat_intelligence_chat_history"

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SUPPORTED_KNOWLEDGE_SOURCES = (
    "mitre_attack",
    "cert_in",
    "cve_database",
    "nvd",
)
