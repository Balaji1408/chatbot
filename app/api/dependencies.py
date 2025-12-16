from app.services.ingestion import IngestionService
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService

# Singleton instances (naive implementation for local usage)
_vector_store_service = VectorStoreService()
_llm_service = LLMService()
_ingestion_service = IngestionService()

def get_vector_store_service() -> VectorStoreService:
    return _vector_store_service

def get_llm_service() -> LLMService:
    return _llm_service

def get_ingestion_service() -> IngestionService:
    return _ingestion_service
