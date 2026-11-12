"""Load runtime settings from the environment and a local .env file."""

import os

from dotenv import load_dotenv

load_dotenv()

# Required to call the chat model. Leave empty to fail fast with a clear error.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Chat model used by the agent loop.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Local embedding model used to index and search document chunks.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Directory where the Chroma vector store is persisted.
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
