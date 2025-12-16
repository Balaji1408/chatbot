# 🧠 Cortex RAG - Project Overview

An elegant, local-first Enterprise GenAI Assistant powered by Retrieval-Augmented Generation (RAG).

## 🛠️ Tech Stack

### Frontend
-   **HTML5 / CSS3**: Custom "Glassmorphism" UI with dark mode, responsive design, and animations.
-   **JavaScript**: Vanilla JS for dynamic DOM manipulation, file handling, and streaming chat responses.
-   **No Frameworks**: Pure, lightweight implementation without React or Vue overhead.

### Backend
-   **Python 3.10+**
-   **FastAPI**: High-performance async web framework.
-   **Uvicorn**: ASGI server for production-grade performance.

### AI & RAG Engine
-   **Ollama**: Local LLM runner (server-less privacy).
-   **LangChain**: Orchestration framework for RAG pipelines.
-   **FAISS**: High-speed local vector storage for document embeddings.
-   **HuggingFace**: `sentence-transformers` for creating high-quality text embeddings.

---

## 🚀 How It Works

1.  **Ingestion (Upload)**
    *   You upload a document (PDF, TXT, DOCX) via the UI.
    *   The backend splits the text into small, meaningful "chunks".
    *   These chunks are converted into mathematical vectors (embeddings) and stored in the local **FAISS** index.

2.  **Retrieval (Chat)**
    *   You ask a question in the chat bar.
    *   The system mathematically searches your uploaded documents for the most relevant text chunks (Context).
    *   You can filter context to "All Documents" or specific files.

3.  **Generation (Answer)**
    *   The relevant context + your question are sent to the local **Ollama** model.
    *   The AI generates a strict answer based *only* on your provided documents.
    *   The response is streamed back to the UI in real-time.

## 🌟 Key Features
-   **Multi-File Support**: Upload and query multiple documents at once.
-   **Context Switching**: Choose exactly which file to chat with.
-   **100% Local**: No data leaves your machine; works offline.
-   **Citations**: See exactly which source document provided the answer.
