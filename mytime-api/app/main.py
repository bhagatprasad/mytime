# app/main.py - WITH AUTH MIDDLEWARE
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import os

# Import settings
from app.core.config import settings

# Import middleware
from app.api.middleware import AuthHeaderMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ========== CREATE APP FIRST ==========
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MyTime AI Integration API with SQL Server",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None
)

# ========== ADD MIDDLEWARE ==========
# 1. CORS Middleware
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

# 2. Auth Header Middleware (ADD THIS!)
app.add_middleware(AuthHeaderMiddleware)

# 3. Trusted Host Middleware (for production)
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["mytime-fastapi.onrender.com", "localhost"]
    )

# ========== BASIC ENDPOINTS ==========
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

# ========== API ROUTE SETUP ==========
def setup_api_routes():
    """Setup API routes - called from startup event"""
    print("=" * 60)
    print("SETTING UP API ROUTES")
    print("=" * 60)
    
    try:
        # Import and include API router
        from app.api.v1.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        print(f"✅ API routes loaded at {settings.API_V1_STR}")
        
        # List routes
        print("\nREGISTERED ROUTES:")
        for route in app.routes:
            if hasattr(route, "path"):
                methods = getattr(route, 'methods', ['GET'])
                print(f"  {route.path} -> {methods}")
                
    except ImportError as e:
        print(f"❌ API import error: {e}")
        # Create fallback routes
        from fastapi import APIRouter
        fallback_router = APIRouter()
        
        @fallback_router.get("/test")
        async def test():
            return {"message": "Fallback API endpoint"}
            
        @fallback_router.get("/users")
        async def users():
            return {"users": ["user1", "user2"]}
            
        app.include_router(fallback_router, prefix="/api/v1")
        print("✅ Fallback routes created at /api/v1")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

# ========== STARTUP EVENT ==========
@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT.value}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Test database connection
    if settings.DATABASE_URL:
        try:
            from app.core.database import test_connection
            if test_connection():
                logger.info("✅ Database connection successful")
            else:
                logger.error("❌ Database connection failed!")
        except Exception as e:
            logger.error(f"⚠️  Error testing database: {str(e)}")
    
    # Setup API routes
    setup_api_routes()

# ========== DIRECT TEST ENDPOINT ==========
@app.get("/direct-test")
async def direct_test():
    return {"message": "Direct test endpoint", "api_status": "Check /api/v1/test"}

# ========== DEBUG AUTH ENDPOINT ==========
@app.get("/debug/auth-test")
async def debug_auth():
    """Debug endpoint to test middleware"""
    return {
        "message": "Auth middleware test",
        "middleware": "AuthHeaderMiddleware is active",
        "check_auth": "Use /api/v1/protected-test for auth test"
    }

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.is_development
    )