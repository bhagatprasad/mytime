# ========== DEBUG: API ROUTER IMPORT ==========
# Move all this code into a function:

def setup_api_routes():
    """Setup API routes separately to avoid circular imports"""
    print("=" * 60)
    print("DEBUG: SETTING UP API ROUTES")
    print("=" * 60)
    
    try:
        # Step 1: Debug the import chain
        print("1. Testing Python path...")
        print(f"   Current dir: {os.getcwd()}")
        
        print("\n2. Trying to import routers module...")
        import app.api.v1.routers
        print("✅ SUCCESS: routers module imported")
        
        print("\n3. Trying to import api_router...")
        from app.api.v1.api import api_router
        print("✅ SUCCESS: api_router imported")
        
        print("\n4. Including API router...")
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
        print(f"\n❌ IMPORT ERROR: {e}")
        print("\nCreating fallback API routes...")
        
        # Create fallback API routes
        from fastapi import APIRouter
        fallback_router = APIRouter()
        
        @fallback_router.get("/test")
        async def api_test():
            return {"message": "Fallback API endpoint", "status": "working"}
        
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

# Call it AFTER app is created
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
