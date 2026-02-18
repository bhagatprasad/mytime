from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Dict, List, Optional, Any, Union
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
    
    # CORS - Define as Union type to accept both string and list
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost:4200,http://127.0.0.1:4200,http://localhost:3000,http://localhost:8080,http://localhost:8000"
    
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
    
    # ============ BACKBLAZE B2 STORAGE ============
    B2_ENDPOINT: str = "s3.us-east-005.backblazeb2.com"
    B2_KEY_ID: str = "332633bece97"
    B2_APP_KEY: str = "00537f0af2eea022537d2605ef4ed7557424c2b859"
    B2_BUCKET_NAME: str = "mytime"
    B2_BUCKET_ID: str = "9393a26623636bce9cce0917"
    B2_REGION: str = "us-east-005"
    B2_PUBLIC_URL: str ="https://mytime.s3.us-east-005.backblazeb2.com"
    B2_MAX_FILE_SIZE_MB: int = 100
    B2_ALLOWED_FILE_TYPES: Union[str, List[str]] = "application/pdf,image/jpeg,image/jpg,image/png,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/plain"
    ENABLE_B2_STORAGE: bool = True

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
    BUSINESS_RSS_FEEDS: Union[str, Dict[str, str]] = '{"economictimes":"https://economictimes.indiatimes.com/rssfeedsdefault.cms","mint":"https://www.livemint.com/rss/companies","business_standard":"https://www.business-standard.com/rss/home_page_top_stories.rss"}'
    
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
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list"""
        if isinstance(self.ALLOWED_ORIGINS, list):
            return self.ALLOWED_ORIGINS
        
        if isinstance(self.ALLOWED_ORIGINS, str):
            origins_str = self.ALLOWED_ORIGINS.strip()
            
            # Handle empty string
            if not origins_str:
                return ["*"] if self.is_development else []
            
            # Try to parse as JSON
            if origins_str.startswith("[") and origins_str.endswith("]"):
                try:
                    return json.loads(origins_str)
                except json.JSONDecodeError:
                    pass
            
            # Parse as comma-separated string
            origins = []
            for origin in origins_str.split(','):
                origin = origin.strip()
                # Remove quotes if present
                origin = origin.strip('"').strip("'").strip()
                if origin and origin not in origins:
                    origins.append(origin)
            return origins
        
        return ["*"] if self.is_development else []
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def validate_allowed_origins(cls, v: Any) -> Any:
        """Convert list to string if needed"""
        if isinstance(v, list):
            return ','.join(v)
        return v
    
    @field_validator('BUSINESS_RSS_FEEDS', mode='before')
    @classmethod
    def validate_rss_feeds(cls, v: Any) -> Any:
        """Convert dict to JSON string if needed"""
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()