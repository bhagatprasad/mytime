# app/main.py - CORRECTED VERSION WITH WORKING CORS
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
import os
import json

# Import settings
from app.core.config import settings

# Import middleware
try:
    from app.core.middleware import AuthHeaderMiddleware
    MIDDLEWARE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  AuthHeaderMiddleware not available: {e}")
    MIDDLEWARE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ========== CORS ORIGINS PARSER ==========
def parse_cors_origins(origins_input):
    """
    Parse CORS origins from various formats.
    Handles: JSON array, comma-separated, space-separated, newline-separated
    """
    if origins_input is None:
        return ["*"]
    
    # If already a list, return as is
    if isinstance(origins_input, list):
        return origins_input
    
    if not isinstance(origins_input, str):
        return ["*"]
    
    origins_str = origins_input.strip()
    
    # Empty string
    if not origins_str:
        return ["*"] if settings.is_development else []
    
    # Try to parse as JSON array
    if origins_str.startswith("[") and origins_str.endswith("]"):
        try:
            # Clean the string first
            clean_str = origins_str.replace("\n", "").replace("\r", "").replace(" ", "")
            parsed = json.loads(clean_str)
            if isinstance(parsed, list):
                # Filter out empty strings and None
                result = [item for item in parsed if item and isinstance(item, str)]
                return result if result else ["*"] if settings.is_development else []
        except json.JSONDecodeError:
            # If JSON parsing fails, continue with string parsing
            pass
    
    # Clean up the string for other formats
    # Remove brackets and quotes
    clean_str = origins_str
    for char in ['[', ']', '{', '}', '"', "'"]:
        clean_str = clean_str.replace(char, "")
    
    # Try different separators
    separators = [',', '\n', ';', ' ']
    for sep in separators:
        if sep in clean_str:
            parts = clean_str.split(sep)
            result = []
            for part in parts:
                part = part.strip()
                if part and part not in result:
                    result.append(part)
            return result if result else ["*"] if settings.is_development else []
    
    # Single origin
    return [origins_str]

# ========== CREATE APP ==========
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MyTime AI Integration API with SQL Server",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None
)

# ========== CORS MIDDLEWARE SETUP ==========
# Parse allowed origins
raw_origins = getattr(settings, 'ALLOWED_ORIGINS', None)
allowed_origins = parse_cors_origins(raw_origins)

# Debug output
print("=" * 60)
print("CORS CONFIGURATION:")
print(f"Raw ALLOWED_ORIGINS from settings: {raw_origins}")
print(f"Parsed allowed origins: {allowed_origins}")
print(f"Number of origins: {len(allowed_origins)}")
print(f"Contains frontend URL: {'https://mytime-ui.netlify.app' in allowed_origins}")
print("=" * 60)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "X-API-Key",
        "X-Client-ID",
        "X-Request-ID"
    ],
    expose_headers=[
        "Content-Disposition",
        "Content-Length",
        "Content-Range",
        "X-Content-Range"
    ],
    max_age=600  # Cache preflight requests for 10 minutes
)

# ========== OTHER MIDDLEWARE ==========
# 2. Auth Header Middleware (with safety check)
if MIDDLEWARE_AVAILABLE:
    try:
        app.add_middleware(AuthHeaderMiddleware)
        print("✅ AuthHeaderMiddleware added successfully")
    except Exception as e:
        print(f"⚠️  Failed to add AuthHeaderMiddleware: {e}")
        # Continue without middleware
else:
    print("⚠️  Running without AuthHeaderMiddleware")

# 3. Trusted Host Middleware (for production)
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["mytime-fastapi.onrender.com", "localhost", "127.0.0.1", "mytime-docker.onrender.com"]
    )

# ========== CORS DEBUG & TEST ENDPOINTS ==========
@app.get("/debug/cors")
async def debug_cors(request: Request):
    """Debug CORS configuration"""
    return {
        "cors_enabled": True,
        "allowed_origins": allowed_origins,
        "request_origin": request.headers.get("origin"),
        "is_allowed": request.headers.get("origin") in allowed_origins,
        "frontend_url": "https://mytime-ui.netlify.app",
        "environment": settings.ENVIRONMENT.value,
        "debug_mode": settings.DEBUG
    }

@app.get("/cors-test")
async def cors_test(request: Request):
    """Simple test endpoint for CORS"""
    return {
        "message": "CORS test successful",
        "origin": request.headers.get("origin"),
        "timestamp": os.times().user
    }

# Handle OPTIONS requests for all paths
@app.options("/{path:path}")
async def handle_options(path: str, request: Request):
    """
    Handle OPTIONS (preflight) requests for all paths.
    This is crucial for CORS to work properly.
    """
    return {
        "message": "Preflight OK",
        "path": path,
        "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        "request_origin": request.headers.get("origin"),
        "status": "allowed" if request.headers.get("origin") in allowed_origins else "blocked"
    }

# ========== BASIC ENDPOINTS ==========
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT.value,
        "cors_enabled": True,
        "cors_origins_count": len(allowed_origins),
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health",
        "debug_cors": "/debug/cors"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT.value,
        "cors": "enabled",
        "timestamp": os.times().user
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"pong": True, "timestamp": os.times().user}

# ========== DEBUG ENDPOINTS ==========
@app.get("/debug/middleware")
async def debug_middleware():
    """Debug middleware status"""
    return {
        "middleware_available": MIDDLEWARE_AVAILABLE,
        "middleware_active": MIDDLEWARE_AVAILABLE,
        "cors_origins": allowed_origins,
        "message": "AuthHeaderMiddleware is active" if MIDDLEWARE_AVAILABLE else "Running without AuthHeaderMiddleware"
    }

@app.get("/direct-test")
async def direct_test():
    return {"message": "Direct test endpoint", "api_status": "Check /api/v1/test"}

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
        
        # Add OPTIONS handler for API routes
        @app.options(f"{settings.API_V1_STR}/{{path:path}}")
        async def api_options_handler(path: str, request: Request):
            return {
                "message": "API preflight OK",
                "api_version": "v1",
                "path": path,
                "allowed": True
            }
        
        # List routes
        print("\nREGISTERED ROUTES:")
        route_count = 0
        for route in app.routes:
            if hasattr(route, "path"):
                methods = getattr(route, 'methods', ['GET'])
                print(f"  {route.path} -> {methods}")
                route_count += 1
        print(f"Total routes: {route_count}")
        
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
            
        @fallback_router.post("/auth/AuthenticateUser")
        async def authenticate_user():
            return {"message": "Authentication endpoint", "status": "mock"}
            
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
    logger.info(f"CORS origins configured: {len(allowed_origins)} origins")
    
    # Display CORS info
    if "https://mytime-ui.netlify.app" in allowed_origins:
        logger.info("✅ Frontend origin (https://mytime-ui.netlify.app) is allowed")
    else:
        logger.warning("⚠️  Frontend origin (https://mytime-ui.netlify.app) is NOT in allowed origins!")
        logger.warning(f"Allowed origins: {allowed_origins}")
    
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

# ========== SHUTDOWN EVENT ==========
@app.on_event("shutdown")
async def shutdown_event():
    """Handle shutdown events"""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    import uvicorn
    
    # Determine host and port
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "=" * 60)
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📡 Host: {host}:{port}")
    print(f"🌍 Environment: {settings.ENVIRONMENT.value}")
    print(f"🔧 Debug: {settings.DEBUG}")
    print(f"🌐 CORS Origins: {allowed_origins}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=settings.is_development,
        log_level="info" if settings.is_development else "warning"
    )