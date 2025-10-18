"""
Configuration management for DataDeck application.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "DataDeck"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # OpenAI (Optional for development - required for AI features)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000
    
    # File Storage
    STORAGE_TYPE: str = "local"
    UPLOAD_DIR: str = "./data/uploads"
    TEMPLATE_DIR: str = "./data/templates"
    REPORT_DIR: str = "./data/reports"
    
    # S3/MinIO
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET_NAME: str = "datadeck"
    S3_REGION: str = "us-east-1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/datadeck.log"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: str = ".xlsx,.xls,.csv"

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [i.strip() for i in self.CORS_ORIGINS.split(",")]

    def get_allowed_extensions(self) -> List[str]:
        """Parse allowed extensions from comma-separated string"""
        return [i.strip() for i in self.ALLOWED_EXTENSIONS.split(",")]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

