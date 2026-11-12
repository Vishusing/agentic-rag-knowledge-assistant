"""Persistent vector store and the embedding model that feeds it."""

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import CHROMA_PATH, EMBEDDING_MODEL

_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    "knowledge_base",
    metadata={"hnsw:space": "cosine"},
)
_embedder = None


def embedder():
    """Load the sentence-transformer on first use and reuse it after that."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
    return _embedder


def collection():
    """Return the Chroma collection that stores document chunks."""
    return _collection
