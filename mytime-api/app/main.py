# app/main.py - UPDATED WITH DEBUG
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import os
import sys

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

# ========== DEBUG: API ROUTER IMPORT ==========
print("=" * 60)
print("DEBUG: STARTING API ROUTER IMPORT")
print("=" * 60)

try:
    # Step 1: Debug the import chain
    print("1. Testing Python path...")
    print(f"   Current dir: {os.getcwd()}")
    print(f"   Files in current dir: {os.listdir('.')}")
    
    print("\n2. Trying to import routers module...")
    import app.api.v1.routers
    print("✅ SUCCESS: routers module imported")
    print(f"   Contents of routers module: {dir(app.api.v1.routers)}")
    
    print("\n3. Checking if auth module exists...")
    if hasattr(app.api.v1.routers, 'auth'):
        print("✅ SUCCESS: auth module found")
        auth_module = app.api.v1.routers.auth
        print(f"   Contents of auth module: {dir(auth_module)}")
        
        if hasattr(auth_module, 'router'):
            print("✅ SUCCESS: auth.router exists")
        else:
            print("❌ ERROR: auth.router NOT found!")
            print("   Creating temporary router...")
            from fastapi import APIRouter
            auth_module.router = APIRouter()
    else:
        print("❌ ERROR: auth module NOT found in routers!")
        
    print("\n4. Trying to import api_router...")
    from app.api.v1.api import api_router
    print("✅ SUCCESS: api_router imported")
    
    print("\n5. Including API router...")
    app.include_router(api_router, prefix=settings.API_V1_STR)
    print(f"✅ SUCCESS: API router included at prefix: {settings.API_V1_STR}")
    
    # List registered routes
    print("\n" + "=" * 60)
    print("REGISTERED ROUTES:")
    route_count = 0
    for route in app.routes:
        if hasattr(route, "path"):
            methods = getattr(route, 'methods', ['GET'])
            print(f"  {route.path} -> {methods}")
            route_count += 1
    print(f"Total routes: {route_count}")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n❌ CRITICAL IMPORT ERROR: {e}")
    print("\nCreating fallback API routes...")
    
    # Create fallback API routes
    from fastapi import APIRouter
    fallback_router = APIRouter()
    
    @fallback_router.get("/test")
    async def api_test():
        return {"message": "Fallback API endpoint", "status": "working"}
    
    @fallback_router.get("/users")
    async def get_users():
        return {"users": ["user1", "user2"], "count": 2}
    
    @fallback_router.get("/auth/login")
    async def login():
        return {"message": "Login endpoint (fallback)"}
    
    app.include_router(fallback_router, prefix="/api/v1")
    print("✅ Fallback API routes created at /api/v1")
    
    import traceback
    logger.error(f"API router import failed, using fallback: {e}\n{traceback.format_exc()}")
    
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    logger.error(f"Unexpected error in API setup: {e}\n{traceback.format_exc()}")

print("=" * 60)
print("DEBUG: API SETUP COMPLETE")
print("=" * 60)

# Add a direct test endpoint
@app.get("/direct-test")
async def direct_test():
    return {"message": "Direct test endpoint", "api_status": "Check /api/v1/test"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.is_development
    )