from pydantic_settings import BaseSettings
from typing import Dict, List, Optional
from enum import Enum

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
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000"
    ]
    
    # ============ DATABASE ============
    DATABASE_URL: str = "mssql+pyodbc://olc_db_usr:DubaiDutyFree@2025@104.243.32.43/Claritydb?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO_SQL: bool = False
    
    # ============ SECURITY ============
    SECRET_KEY: str = "I9JohndoejanemariasmithBobsanchezcharliedavidson"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12
    
    # ============ AI/ML SERVICES ============
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ORGANIZATION: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
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
        "moneycontrol": "https://www.moneycontrol.com/rss/buzzingstocks.xml",
        "ndtv_profit": "https://feeds.feedburner.com/ndtvprofit-latest",
        "reuters_business": "http://feeds.reuters.com/news/wealth",
        "bloomberg": "https://www.bloomberg.com/feeds/podcasts/etf_report.xml",
        "forbes": "https://www.forbes.com/business/feed/"
    }
    
    # ============ FEATURE FLAGS ============
    ENABLE_AI_ANALYSIS: bool = True
    ENABLE_RSS_FEEDS: bool = True
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 300
    
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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()