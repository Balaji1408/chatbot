import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise GenAI Assistant"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    DOCS_DIR: str = os.path.join(DATA_DIR, "docs")
    VECTOR_STORE_DIR: str = os.path.join(DATA_DIR, "vector_store")
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM Settings (Ollama - Legacy/Local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3.2:1b"
    
    # AWS Bedrock Settings
    USE_AWS_BEDROCK: bool = True
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "meta.llama3-70b-instruct-v1:0" 
    BEDROCK_EMBEDDING_MODEL_ID: str = "amazon.titan-embed-text-v1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Google Gemini Settings (Free Tier Available)
    USE_GEMINI: bool = False
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DOCS_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
