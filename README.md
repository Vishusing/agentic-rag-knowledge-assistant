# Agentic RAG Knowledge Assistant

A portfolio-ready project combining Generative AI, Retrieval-Augmented Generation (RAG), and agentic tool use.

## Features
- Upload PDF, DOCX, TXT, and Markdown documents.
- Extract, chunk, embed, and index content in persistent ChromaDB.
- Retrieve semantically relevant passages and answer with source citations.
- Let the LLM choose tools: knowledge-base search, safe calculator, and document inventory.
- Inspect the agent's tool trace in the Streamlit UI.
- FastAPI backend with interactive API docs.

## Resume-ready description
**Agentic RAG Knowledge Assistant | Python, OpenAI, FastAPI, Streamlit, ChromaDB, Sentence Transformers**
- Built a document-grounded GenAI assistant using text extraction, chunking, vector embeddings, and semantic retrieval.
- Implemented an agentic tool-calling loop that selects retrieval, calculator, and document-inventory tools based on user intent.
- Added source-aware responses with document/page references to improve traceability and reduce unsupported answers.
- Developed a Streamlit chat interface and FastAPI ingestion/query service.

Do not claim performance improvements until you have measured them.

## Architecture
Streamlit UI → FastAPI → Agent orchestrator → (RAG retrieval / calculator / document inventory)
RAG pipeline → Sentence Transformers embeddings → ChromaDB vector store

## Run locally
1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your OpenAI API key.
5. Start API: `uvicorn app.api:app --reload`
6. In another terminal start UI: `streamlit run app/ui/main.py`
7. Open the Streamlit URL printed in the terminal. API docs: http://127.0.0.1:8000/docs

## Demo
Upload a technical PDF or course notes. Ask a question and inspect citations. Then ask "What is 18% of 2450?" to trigger the calculator, or "List my uploaded files" to trigger inventory.

## Evaluation ideas
Build a 20–50 question test set and measure Retrieval Recall@K, citation accuracy, faithfulness, tool-selection accuracy, latency, and token cost. Add a reranker, hybrid BM25/vector search, and an evaluation dashboard as future work.

## Safety
Uploaded content is untrusted evidence, not instructions. The calculator uses a restricted AST evaluator (not `eval`). The agent has a bounded tool loop. Avoid uploading confidential documents unless you understand your provider's data-handling settings.
