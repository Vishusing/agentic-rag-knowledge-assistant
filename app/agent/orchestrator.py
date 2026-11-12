"""Run the chat model in a bounded loop that can call tools."""

import json

from openai import OpenAI

from app.agent.definitions import TOOLS
from app.agent.prompts import SYSTEM
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.tools import run_tool

# Stop the model from calling tools forever, and keep only a short chat history.
MAX_TOOL_ROUNDS = 5
HISTORY_LIMIT = 8


def _history_messages(history):
    """Turn recent user and assistant turns into chat messages."""
    messages = []
    for item in (history or [])[-HISTORY_LIMIT:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content})
    return messages


def _execute_tool_calls(message, messages, trace):
    """Run every tool the model requested and append each result to the transcript."""
    messages.append(message)
    for call in message.tool_calls:
        name = call.function.name
        arguments = json.loads(call.function.arguments or "{}")
        try:
            result = run_tool(name, arguments)
        except Exception as exc:
            result = {"error": str(exc)}
        trace.append({"tool": name, "arguments": arguments, "result": result})
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": json.dumps(result, ensure_ascii=False),
        })



def ask_agent(question: str, history=None):
    """Answer a question using an agentic tool-calling loop."""

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing.")

    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    messages = [{"role": "system", "content": SYSTEM}]
    messages.extend(_history_messages(history))
    messages.append({"role": "user", "content": question})

    trace = []

    for _ in range(MAX_TOOL_ROUNDS):

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=1000,
            )

        except Exception as e:
            print("OPENAI API ERROR:", repr(e))
            raise

        message = response.choices[0].message

        if not message.tool_calls:
            return {
                "answer": message.content or "",
                "tool_trace": trace
            }

        _execute_tool_calls(message, messages, trace)

    messages.append({
        "role": "user",
        "content": "Answer concisely now. Do not call more tools."
    })

    final = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1000,
    )

    return {
        "answer": final.choices[0].message.content or "",
        "tool_trace": trace
    }
