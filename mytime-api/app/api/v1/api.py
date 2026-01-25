# app/api/v1/api.py - Ensure this has authorization
from fastapi import APIRouter, Depends

print("=" * 50)
print("DEBUG: Loading api.py with authorization")
print("=" * 50)

# Try to import get_current_user
try:
    from app.core.dependencies import get_current_user
    HAS_AUTH = True
    print("✅ get_current_user imported successfully")
except ImportError as e:
    HAS_AUTH = False
    print(f"⚠️  get_current_user import failed: {e}")
    
    # Create a dummy dependency for development
    async def get_current_user():
        return {"username": "test", "roles": ["admin"]}

# Import routers
try:
    from app.api.v1.routers import auth, user, roles, llm, vision, audio, embeddings, rss, country
    print("✅ All routers imported")
except ImportError as e:
    print(f"❌ Router import error: {e}")
    # Create dummy routers for development
    from fastapi import APIRouter
    
    class DummyRouter:
        def __init__(self):
            self.router = APIRouter()
    
    auth = DummyRouter()
    user = DummyRouter()
    roles = DummyRouter()
    llm = DummyRouter()
    vision = DummyRouter()
    audio = DummyRouter()
    embeddings = DummyRouter()
    rss = DummyRouter()
    country = DummyRouter()

# Create main router
api_router = APIRouter()

# Public routes - authentication should be public
api_router.include_router(auth.router, tags=["authentication"])

# Protected routes
if HAS_AUTH:
    from fastapi import APIRouter
    
    # Create protected routers with dependencies
    users_protected = APIRouter(dependencies=[Depends(get_current_user)])
    users_protected.include_router(user.router)
    
    roles_protected = APIRouter(dependencies=[Depends(get_current_user)])
    roles_protected.include_router(roles.router)
    
    countries_protected = APIRouter(dependencies=[Depends(get_current_user)])
    countries_protected.include_router(country.router)
    
    # Include protected routes
    api_router.include_router(users_protected, prefix="/users", tags=["users"])
    api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])
    api_router.include_router(countries_protected, prefix="/countries", tags=["countries"])
else:
    # Development mode - include without auth
    api_router.include_router(user.router, prefix="/users", tags=["users"])
    api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
    api_router.include_router(country.router, prefix="/countries", tags=["countries"])

# AI routes - decide if these should be public or protected
# For now, making them public for development
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss.router, prefix="/rss", tags=["rss"])

# Test endpoints
@api_router.get("/test", tags=["test"])
async def api_test():
    return {"message": "API test", "status": "working"}

@api_router.get("/protected-test", tags=["test"])
async def protected_test(current_user = Depends(get_current_user) if HAS_AUTH else None):
    return {
        "message": "Protected endpoint",
        "user": current_user if current_user else "No auth",
        "protected": HAS_AUTH
    }

print(f"✅ API routes loaded at /api/v1")
print(f"✅ Auth enabled: {HAS_AUTH}")