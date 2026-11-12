"""Connect tool names chosen by the model to the functions that run them."""

from app.rag import list_documents, retrieve
from app.tools.calculator import safe_calculate


def run_tool(name: str, arguments: dict):
    """Run one tool by name and return a JSON-serializable result."""
    if name == "search_knowledge_base":
        matches = retrieve(arguments["query"], arguments.get("top_k", 5))
        return {"matches": matches}
    if name == "calculate":
        return {"result": safe_calculate(arguments["expression"])}
    if name == "list_documents":
        return {"documents": list_documents()}
    raise ValueError(f"Unknown tool: {name}")
