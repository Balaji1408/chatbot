from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Source, UploadResponse, DocumentInfo
from app.api.dependencies import get_vector_store_service, get_llm_service, get_ingestion_service
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
from app.services.ingestion import IngestionService
from app.core.config import settings

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):
    try:
        # Process files
        docs = await ingestion_service.process_files(files)
        
        # Add to vector store
        vector_store_service.create_or_update_index(docs)
        
        return UploadResponse(
            message=f"Successfully processed {len(files)} files and indexed {len(docs)} chunks.",
            documents=[DocumentInfo(filename=f.filename, size=0, content_type=f.content_type or "unknown") for f in files]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/files", response_model=List[str])
async def list_files(
    vector_service: VectorStoreService = Depends(get_vector_store_service)
):
    return vector_service.list_sources()

from fastapi.responses import StreamingResponse
import json

@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    vector_service: VectorStoreService = Depends(get_vector_store_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    # 1. Retrieve relevant docs (Increased k for effectiveness)
    relevant_docs = vector_service.search(request.question, k=5, filter_source=request.selected_file)
    
    # 2. Generator function
    async def response_generator():
        try:
            # Stream the answer tokens
            async for token in llm_service.generate_answer_stream(request.question, relevant_docs):
                yield token
        except Exception as e:
            yield f"\n\n[Error generating response: {str(e)}]"
            
        # Send sources at the end
        valid_sources = []
        seen_sources = set()
        for doc in relevant_docs:
            source = doc.metadata.get('source', 'unknown')
            if source in ["Budgie_User Manual &FAQ.pdf", "Budgie CE User Manual & FAQ.pdf", "Budgie CE User Manual & FAQ.pdf.pdf"]:
                continue
            if source not in seen_sources:
                valid_sources.append(source)
                seen_sources.add(source)
        
        if valid_sources:
            yield "\n\n**Sources:**\n"
            for source in valid_sources:
                yield f"- {source}\n"

    return StreamingResponse(response_generator(), media_type="text/plain")

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    vector_service: VectorStoreService = Depends(get_vector_store_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    # Retrieve more docs for better context
    relevant_docs = vector_service.search(request.question, k=5, filter_source=request.selected_file) 
    
    # Generate full answer (legacy non-streaming)
    answer = ""
    async for chunk in llm_service.generate_answer_stream(request.question, relevant_docs):
        answer += chunk
        
    sources = [
        Source(source=doc.metadata.get("source", "unknown"), page_content=doc.page_content) 
        for doc in relevant_docs
        if doc.metadata.get("source", "unknown") not in ["Budgie_User Manual &FAQ.pdf", "Budgie CE User Manual & FAQ.pdf", "Budgie CE User Manual & FAQ.pdf.pdf"]
    ]
    
    return ChatResponse(answer=answer, sources=sources)

@router.delete("/reset")
async def reset_database(vector_service: VectorStoreService = Depends(get_vector_store_service)):
    vector_service.clear()
    return {"message": "Knowledge base cleared."}
