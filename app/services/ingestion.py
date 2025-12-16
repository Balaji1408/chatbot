import os
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import settings
import shutil

class IngestionService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )

    async def save_upload_file(self, upload_file: UploadFile) -> str:
        file_path = os.path.join(settings.DOCS_DIR, upload_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return file_path

    def load_document(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return loader.load()

    async def process_files(self, files: List[UploadFile]) -> List[Document]:
        all_chunks = []
        for file in files:
            # Save file locally
            file_path = await self.save_upload_file(file)
            
            # Load content
            documents = self.load_document(file_path)
            
            # Add metadata if missing
            for doc in documents:
                doc.metadata["source"] = file.filename
            
            # Split chunks
            chunks = self.text_splitter.split_documents(documents)
            all_chunks.extend(chunks)
            
        return all_chunks
