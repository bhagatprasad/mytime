from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MyTime AI Integration API",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None
)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://mytime-ui.netlify.app"
]

print(f"✅ CORS Origins configured: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

@app.options("/api/v1/auth/AuthenticateUser")
async def auth_options():
    return {}

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "cors_enabled": True,
        "origins": origins
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "cors": "enabled"
    }

def setup_api_routes():
    try:
        from app.api.v1.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        print(f"✅ API routes loaded at {settings.API_V1_STR}")
    except Exception as e:
        print(f"❌ API import error: {e}")

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    setup_api_routes()