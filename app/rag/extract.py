"""Read uploaded files into plain text."""

import io
from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_text(filename: str, data: bytes):
    """Read a PDF, DOCX, TXT, or Markdown file into (location, text) pairs.

    PDFs are split by page. Other formats return one block labeled "document".
    """
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(data))
        pages = []
        for index, page in enumerate(reader.pages):
            pages.append((f"page {index + 1}", page.extract_text() or ""))
        return pages

    if suffix == ".docx":
        document = DocxDocument(io.BytesIO(data))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        return [("document", text)]

    if suffix in {".txt", ".md"}:
        return [("document", data.decode("utf-8", errors="replace"))]

    raise ValueError("Supported formats: PDF, DOCX, TXT, MD")
