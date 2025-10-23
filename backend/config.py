"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "dev-secret-key-change-in-production"
    environment: str = "development"
    debug: bool = True
    api_title: str = "MyNaga Dashboard API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
