"""Split long text into overlapping chunks for embedding."""


def chunk_text(text: str, size: int = 850, overlap: int = 140):
    """Break text into word windows so retrieval can match a smaller passage.

    Each next window starts `overlap` words before the previous one ended.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap

    return chunks
