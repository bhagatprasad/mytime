from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import os

# Import settings
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MyTime AI Integration API with SQL Server",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None
)

# Configure CORS - Fix for list parsing
cors_origins = settings.ALLOWED_ORIGINS
if isinstance(cors_origins, str):
    # Handle string from environment variable
    cors_origins = [origin.strip() for origin in cors_origins.strip("[]").replace('"', '').replace("'", "").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["mytime-fastapi.onrender.com", "localhost"]
    )

@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT.value}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Test database connection only if DATABASE_URL is set
    if settings.DATABASE_URL:
        try:
            from app.core.database import test_connection
            if test_connection():
                logger.info("✅ Database connection successful")
            else:
                logger.error("❌ Database connection failed!")
        except ImportError:
            logger.warning("⚠️  Database module not found")
        except Exception as e:
            logger.error(f"⚠️  Error testing database: {str(e)}")
    else:
        logger.warning("⚠️  DATABASE_URL not set, skipping database connection")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT.value,
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT.value
    }

# Import and include API router
try:
    from app.api.v1.api import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
except ImportError:
    logger.warning("API router not found. Starting without API routes.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.is_development
    )