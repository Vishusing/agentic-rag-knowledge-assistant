"""JSON schemas the model sees when it decides which tool to call."""

# Each entry is an OpenAI function tool. The names must match app.tools.dispatch.run_tool.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search uploaded documents for evidence relevant to a question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 8},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform basic arithmetic when a question requires calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_documents",
            "description": "List names of all uploaded documents.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]
