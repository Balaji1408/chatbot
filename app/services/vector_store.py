import os
from typing import List, Tuple
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.core.config import settings

class VectorStoreService:
    def __init__(self):
        if settings.USE_AWS_BEDROCK:
            # Use AWS Bedrock Embeddings
            from langchain_aws import BedrockEmbeddings
            import boto3
            
            boto3_session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            self.embeddings = BedrockEmbeddings(
                client=boto3_session.client("bedrock-runtime"),
                model_id=settings.BEDROCK_EMBEDDING_MODEL_ID
            )
        elif settings.USE_GEMINI:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GEMINI_API_KEY
            )
        else:
            # Fallback to Local HuggingFace
            self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            
        self.vector_store = None
        self.load_index()

    def load_index(self):
        try:
            if os.path.exists(settings.VECTOR_STORE_DIR) and \
               os.path.exists(os.path.join(settings.VECTOR_STORE_DIR, "index.faiss")):
                self.vector_store = FAISS.load_local(
                    settings.VECTOR_STORE_DIR, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                self.vector_store = None
        except Exception as e:
            print(f"Error loading vector store: {e}")
            self.vector_store = None

    def create_or_update_index(self, documents: List[Document]):
        if not documents:
            return

        if self.vector_store:
            self.vector_store.add_documents(documents)
        else:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            
        self.vector_store.save_local(settings.VECTOR_STORE_DIR)

    def search(self, query: str, k: int = 4, filter_source: str = None) -> List[Document]:
        if not self.vector_store:
            return []
        
        filter_dict = None
        if filter_source and filter_source != "All Documents":
            filter_dict = {"source": filter_source}
        
        # Similarity search
        return self.vector_store.similarity_search(query, k=k, filter=filter_dict)

    def list_sources(self) -> List[str]:
        if not self.vector_store:
            return []
        try:
            sources = set()
            # Access underlying docstore to find unique sources
            for doc in self.vector_store.docstore._dict.values():
                if 'source' in doc.metadata:
                    sources.add(doc.metadata['source'])
            return sorted(list(sources))
        except Exception as e:
            print(f"Error listing sources: {e}")
            return []

    def clear(self):
        if os.path.exists(settings.VECTOR_STORE_DIR):
            import shutil
            shutil.rmtree(settings.VECTOR_STORE_DIR)
            os.makedirs(settings.VECTOR_STORE_DIR)
        self.vector_store = None
