"""Request bodies accepted by the HTTP API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """A user question plus optional earlier chat turns."""

    question: str = Field(min_length=1, max_length=4000)
    history: list[dict] = []
