"""Index documents and search them by meaning."""

import hashlib

from app.rag.chunking import chunk_text
from app.rag.extract import extract_text
from app.rag.store import collection, embedder


def ingest_file(filename: str, data: bytes):
    """Extract a file, chunk it, embed the chunks, and upsert them into Chroma."""
    ids = []
    documents = []
    metadatas = []
    digest = hashlib.sha1(data).hexdigest()[:12]

    for location, text in extract_text(filename, data):
        for index, chunk in enumerate(chunk_text(text)):
            ids.append(f"{digest}-{len(ids)}")
            documents.append(chunk)
            metadatas.append({
                "source": filename,
                "location": location,
                "chunk": index,
            })

    if not documents:
        raise ValueError("No extractable text found in this file.")

    vectors = embedder().encode(documents, normalize_embeddings=True).tolist()
    collection().upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=vectors,
    )
    return {"filename": filename, "chunks_added": len(documents)}


def retrieve(query: str, top_k: int = 5):
    """Embed a query and return the closest stored chunks with source metadata."""
    count = collection().count()
    if count == 0:
        return []

    vector = embedder().encode([query], normalize_embeddings=True).tolist()[0]
    result = collection().query(
        query_embeddings=[vector],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    rows = zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    )
    for text, metadata, distance in rows:
        matches.append({
            "text": text,
            "source": metadata.get("source", "unknown"),
            "location": metadata.get("location", "unknown"),
            "chunk": metadata.get("chunk", -1),
            "score": round(1 - float(distance), 4),
        })
    return matches


def list_documents():
    """Return the sorted unique filenames stored in the collection."""
    rows = collection().get(include=["metadatas"])
    sources = {metadata.get("source", "unknown") for metadata in rows["metadatas"]}
    return sorted(sources)
