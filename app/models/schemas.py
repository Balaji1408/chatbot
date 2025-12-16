from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    selected_file: Optional[str] = None
    history: List[ChatMessage] = []

class Source(BaseModel):
    source: str
    page_content: str
    # metadata: dict

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

class DocumentInfo(BaseModel):
    filename: str
    size: int
    content_type: str

class UploadResponse(BaseModel):
    message: str
    documents: List[DocumentInfo]
