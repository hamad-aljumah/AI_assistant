from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_base_url: str = "https://us.api.openai.com/v1"
    
    # Database
    database_url: str
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "ai_assistant"
    
    # Application
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    upload_dir: str = "./uploads"
    vector_store_dir: str = "./vector_store"
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
