from pydantic_settings import BaseSettings
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import os

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings(BaseSettings):
    # ============ APPLICATION ============
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True
    PROJECT_NAME: str = "MyTime - AI Integration API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS - Handle both list and JSON string
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000"
    ]
    
    # ============ DATABASE ============
    DATABASE_URL: Optional[str] = None  # Set via environment variable
    DATABASE_POOL_SIZE: int = 5  # Lower for Render free tier
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO_SQL: bool = False
    
    # ============ SECURITY ============
    SECRET_KEY: str = "change-this-in-production"  # Will be overridden by env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12
    
    # ============ AI/ML SERVICES ============
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ORGANIZATION: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1000  # Lower for free tier
    DEFAULT_LLM_PROVIDER: str = "openai"
    HUGGINGFACE_TOKEN: Optional[str] = None
    AZURE_OPENAI_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT: Optional[str] = None
    GOOGLE_AI_API_KEY: Optional[str] = None
    GOOGLE_AI_MODEL: str = "gemini-pro"
    
    # ============ RSS FEEDS ============
    BUSINESS_RSS_FEEDS: Dict[str, str] = {
        "economictimes": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
        "mint": "https://www.livemint.com/rss/companies",
        "business_standard": "https://www.business-standard.com/rss/home_page_top_stories.rss",
    }
    
    # ============ FEATURE FLAGS ============
    ENABLE_AI_ANALYSIS: bool = True
    ENABLE_RSS_FEEDS: bool = True
    ENABLE_CACHE: bool = False  # Disable cache on free tier (no Redis)
    CACHE_TTL: int = 300
    
    # ============ RENDER SPECIFIC ============
    RENDER: bool = True
    PORT: int = 8000
    
    # Computed properties
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == Environment.TESTING
    
    # Custom validator for ALLOWED_ORIGINS
    @classmethod
    def parse_allowed_origins(cls, v: Any) -> List[str]:
        if isinstance(v, list):
            return v
        elif isinstance(v, str):
            try:
                # Try to parse as JSON
                return json.loads(v)
            except json.JSONDecodeError:
                # Parse as comma-separated string
                return [origin.strip() for origin in v.strip("[]").replace('"', '').replace("'", "").split(",")]
        return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()