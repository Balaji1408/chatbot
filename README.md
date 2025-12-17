# Enterprise GenAI Knowledge Assistant

A production-ready, local-first Retrieval-Augmented Generation (RAG) system designed for enterprise use cases. This assistant allows users to upload documents (PDF, DOCX, TXT), processes them into a local vector database, and answers questions with strict grounding and source attribution.

## Features

- **Local-First & Privacy-Focused**: Runs entirely offline using local LLMs (via Ollama) and local vector stores.
- **Multi-Format Ingestion**: Supports PDF, DOCX, and TXT files.
- **Advanced RAG Pipeline**: Implements semantic search with FAISS, context windowing, and strict prompt engineering to reduce hallucinations.
- **Source Attribution**: Every answer provides citations to the specific document and chunk used.
- **Modular Architecture**: Built with FastAPI and a service-layer component design for easy swapping of LLMs or vector databases.

## Technology Stack

- **Backend**: Python 3.9+, FastAPI
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: HuggingFace (Sentence Transformers) locally
- **LLM**: Ollama (Llama 3, Mistral, or similar) or OpenAI-compatible local endpoints.
- **Orchestration**: Custom RAG pipeline (optionally LangChain compatible components).

## Getting Started

### Prerequisites

1.  **Python 3.10+** installed.
2.  **Ollama** installed and running (for the LLM).
    -   `ollama pull llama3` (or your preferred model)

### Installation

1.  Clone the repository (or navigate to directory).
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
2.  Access the API documentation at `http://localhost:8000/docs`.

## Usage API

- **POST /api/upload**: Upload files to ingest.
- **POST /api/chat**: Ask questions against the ingested knowledge base.
- **DELETE /api/reset**: Clear the knowledge base.

## Deployment

- [Free Cloud Deployment Guide (Llama 3 via Groq)](FREE_DEPLOYMENT_GUIDE_GROQ.md)
- [Free Deployment Guide (Gemini)](FREE_DEPLOYMENT_GUIDE_GEMINI.md)

