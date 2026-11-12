"""Public retrieval API used by the HTTP routes and agent tools."""

from app.rag.pipeline import ingest_file, list_documents, retrieve

__all__ = ["ingest_file", "list_documents", "retrieve"]
