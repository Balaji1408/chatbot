# System Architecture

This document outlines the architecture for the Enterprise GenAI Knowledge Assistant.

## High-Level Design

The system follows a typical RAG (Retrieval-Augmented Generation) pattern, broken down into distinct stages: **Ingestion**, **Retrieval**, and **Generation**.

```mermaid
graph TD
    User[User] -->|Upload Docs| API[FastAPI Backend]
    User -->|Query| API
    
    subgraph "Ingestion Pipeline"
        API -->|File| Parser[Document Parser]
        Parser -->|Text| Chunker[Text Splitter]
        Chunker -->|Chunks| Embedder[Embedding Model]
        Embedder -->|Vectors| VectorDB[(FAISS Vector Store)]
    end
    
    subgraph "Retrieval & Generation Pipeline"
        API -->|Query| QueryEmbedder[Embedding Model]
        QueryEmbedder -->|Vector| VectorDB
        VectorDB -->|Top-K Chunks| ContextBuilder[Context Builder]
        ContextBuilder -->|Context + Prompt| LLM[Local LLM (Ollama)]
        LLM -->|Answer + Citations| API
    end
```

## Components

### 1. Ingestion Service
- **Responsibility**: Handles file uploads, text extraction, cleaning, and chunking.
- **Tools**: `pypdf` for PDFs, `python-docx` for Word docs.
- **Strategy**: Recursive character splitting with overlap to maintain context across boundaries.

### 2. Vector Store Service
- **Responsibility**: Manages the FAISS index.
- **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` (fast, local, effective) to convert text chunks into dense vectors.
- **Storage**: Persists the index locally to disk (`data/vector_store/`) to survive restarts.

### 3. LLM Service
- **Responsibility**: Interfaces with the Large Language Model.
- **Implementation**: Connects to a local Ollama instance (default `http://localhost:11434`).
- **Prompting**: Uses a strict system prompt to enforce "Answer based ONLY on context" rules and citation formatting.

### 4. API Layer (FastAPI)
- **Responsibility**: Exposes REST endpoints for the frontend or client applications.
- **State Management**: Manages session state/history (in-memory for this MVP, extensible to Redis/DB).

## Data Flow

1.  **Upload**:
    -   User sends file -> API saves to `data/docs/` -> Ingestion Service reads and chunks -> Embeddings generated -> Stored in FAISS.
2.  **Query**:
    -   User sends question -> Embedding generated for question -> FAISS searches for nearest neighbors -> Relevant text chunks retrieved.
    -   Prompt constructed: `System Instruction + Retrieved Context + User Question`.
    -   LLM generates response.
    -   Response parsed to separate answer from metadata (if needed).

## Directory Structure

```
/
├── app/
│   ├── api/            # Route handlers
│   ├── core/           # Config and Prompts
│   ├── models/         # Pydantic Schemas
│   ├── services/       # Business Logic (Ingest, RAG, LLM)
│   └── main.py         # Entry point
├── data/               # Local storage
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```
