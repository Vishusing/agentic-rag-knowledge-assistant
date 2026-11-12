"""FastAPI application entry point. Run with: uvicorn app.api:app --reload"""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Agentic RAG Knowledge Assistant", version="1.0.0")
app.include_router(router)
