# app/main.py - CORRECTED VERSION WITHOUT DUPLICATE ENDPOINTS
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json

# Import settings
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ========== CREATE APP ==========
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MyTime AI Integration API",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None
)

# ========== CORS MIDDLEWARE - SIMPLIFIED ==========
# Get origins directly from environment variable
origins_str = os.getenv("ALLOWED_ORIGINS", 
    "http://localhost:4200,http://127.0.0.1:4200,http://localhost:3000,http://localhost:8080,http://localhost:8000,https://mytime-ui.netlify.app")

# Parse origins
if isinstance(origins_str, str):
    # Clean and parse
    origins_str = origins_str.strip()
    if origins_str.startswith("[") and origins_str.endswith("]"):
        try:
            origins = json.loads(origins_str)
        except:
            origins = [origin.strip() for origin in origins_str.strip("[]").replace('"', '').replace("'", "").split(",")]
    else:
        origins = [origin.strip() for origin in origins_str.split(",")]
else:
    origins = origins_str

print(f"✅ CORS Origins configured: {origins}")

# Add CORS middleware - SIMPLE AND EFFECTIVE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=600
)

# ========== EXPLICIT OPTIONS HANDLER ==========
@app.options("/{path:path}")
async def preflight_handler(path: str, request: Request):
    """
    Handle ALL OPTIONS (preflight) requests.
    This is CRITICAL for CORS to work.
    """
    origin = request.headers.get("origin")
    return {
        "status": "preflight_allowed",
        "origin": origin,
        "path": path,
        "allowed": origin in origins
    }

# ========== BASIC ENDPOINTS ==========
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

@app.get("/cors-test")
async def cors_test(request: Request):
    origin = request.headers.get("origin")
    return {
        "message": "CORS test",
        "your_origin": origin,
        "allowed": origin in origins if origin else False,
        "all_allowed_origins": origins
    }

# ========== DEBUG ENDPOINTS ==========
@app.get("/debug/headers")
async def debug_headers(request: Request):
    """Debug request headers"""
    return {
        "headers": dict(request.headers),
        "origin": request.headers.get("origin"),
        "method": request.method
    }

# ========== API ROUTE SETUP ==========
def setup_api_routes():
    """Setup API routes - moved authentication to router"""
    print("=" * 60)
    print("SETTING UP API ROUTES")
    print("=" * 60)
    
    try:
        # Import and include API router
        from app.api.v1.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        print(f"✅ API routes loaded at {settings.API_V1_STR}")
        
        # Check if auth endpoint exists in router
        print("\n✅ Authentication endpoints are now handled by the router at:")
        print(f"   POST {settings.API_V1_STR}/auth/AuthenticateUser")
        
    except ImportError as e:
        print(f"⚠️  API import error: {e}")
        print("Creating minimal fallback routes...")
        
        # Create minimal fallback router
        from fastapi import APIRouter
        
        fallback_router = APIRouter()
        
        @fallback_router.get("/test")
        async def test():
            return {"message": "API is working"}
            
        @fallback_router.get("/health")
        async def api_health():
            return {"api": "healthy"}
            
        app.include_router(fallback_router, prefix=settings.API_V1_STR)
        print("✅ Fallback routes created")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

# ========== STARTUP EVENT ==========
@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"🌐 CORS Origins: {origins}")
    
    # Check if frontend URL is allowed
    frontend_url = "https://mytime-ui.netlify.app"
    if frontend_url in origins:
        logger.info(f"✅ Frontend URL '{frontend_url}' is allowed")
    else:
        logger.warning(f"⚠️  Frontend URL '{frontend_url}' is NOT in allowed origins!")
    
    # Setup API routes
    setup_api_routes()

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "=" * 60)
    print(f"Starting server on {host}:{port}")
    print(f"CORS Origins: {origins}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False
    )
