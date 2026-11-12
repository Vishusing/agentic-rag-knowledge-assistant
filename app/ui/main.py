"""Chat interface. This file only talks to the FastAPI server."""

import requests
import streamlit as st

# Base URL of the local API started with uvicorn.
API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Knowledge Assistant", page_icon="🧠", layout="wide")
st.title("🧠 Agentic RAG Knowledge Assistant")
st.caption("Ask questions over your documents with source-grounded answers and agent tools.")


def render_sidebar():
    """Upload files for indexing and show which documents are already stored."""
    st.subheader("Knowledge base")
    uploads = st.file_uploader(
        "Upload PDF, DOCX, TXT, or MD",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )
    if st.button("Index documents", disabled=not uploads, use_container_width=True):
        index_uploads(uploads)
    show_indexed_files()


def index_uploads(uploads):
    """Post the selected files to /ingest and show how many chunks were stored."""
    with st.spinner("Extracting, chunking, and embedding..."):
        try:
            payload = [
                ("files", (file.name, file.getvalue(), "application/octet-stream"))
                for file in uploads
            ]
            response = requests.post(f"{API}/ingest", files=payload, timeout=300)
            response.raise_for_status()
            st.success(response.json()["results"])
        except requests.RequestException as exc:
            st.error(f"Indexing failed: {exc}")


def show_indexed_files():
    """Fetch /documents and list the indexed filenames, or warn if the API is down."""
    try:
        documents = requests.get(f"{API}/documents", timeout=10).json()["documents"]
        st.write("**Indexed files**")
        if documents:
            st.write("\n".join(f"• {name}" for name in documents))
        else:
            st.write("No files indexed yet.")
    except requests.RequestException:
        st.warning("Start the FastAPI server to connect.")


def render_history():
    """Replay saved chat turns, including any agent tool trace."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("trace"):
                with st.expander("Agent tool trace"):
                    st.json(message["trace"])


def answer_question(prompt):
    """Send the question and prior turns to /chat, then store the reply."""
    history = st.session_state.messages[:-1]
    with st.chat_message("assistant"):
        with st.spinner("Thinking and selecting tools..."):
            try:
                response = requests.post(
                    f"{API}/chat",
                    json={"question": prompt, "history": history},
                    timeout=180,
                )
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                trace = data.get("tool_trace", [])
                st.markdown(answer)
                if trace:
                    with st.expander("Agent tool trace"):
                        st.json(trace)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "trace": trace,
                })
            except requests.RequestException as exc:
                st.error(f"Chat failed: {exc}")


with st.sidebar:
    render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

render_history()

prompt = st.chat_input("Ask something about your documents...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    answer_question(prompt)
