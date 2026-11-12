"""HTTP routes for health checks, document indexing, and chat."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.agent import ask_agent
from app.api.schemas import ChatRequest
from app.rag import ingest_file, list_documents

router = APIRouter()


@router.get("/health")
def health():
    """Report that the API process is up."""
    return {"status": "ok"}


@router.get("/documents")
def documents():
    """Return the names of files currently stored in the knowledge base."""
    return {"documents": list_documents()}


@router.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    """Extract, chunk, embed, and index each uploaded file."""
    results = []
    for file in files:
        try:
            contents = await file.read()
            results.append(ingest_file(file.filename or "upload", contents))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
    return {"results": results}


@router.post("/chat")
def chat(request: ChatRequest):
    """Send a question to the agent and return its answer and tool trace."""
    try:
        return ask_agent(request.question, request.history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
