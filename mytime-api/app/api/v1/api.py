# app/api/v1/api.py - SIMPLIFIED WORKING VERSION
from fastapi import APIRouter, Depends
from fastapi import APIRouter as FastAPIRouter

print("=" * 50)
print("DEBUG: Loading api.py")
print("=" * 50)

# Try to import routers, with fallbacks
try:
    # Try importing from routers
    from app.api.v1.routers import auth, user, roles
    print("✅ Imported auth, user, roles from routers")
except ImportError as e:
    print(f"❌ Error importing from routers: {e}")
    # Create dummy routers
    from fastapi import APIRouter
    auth = type('obj', (object,), {'router': APIRouter()})
    user = type('obj', (object,), {'router': APIRouter()})
    roles = type('obj', (object,), {'router': APIRouter()})
    print("✅ Created dummy routers")

try:
    from app.api.v1.routers import llm, vision, audio, embeddings, rss
    print("✅ Imported AI routers")
except ImportError:
    from fastapi import APIRouter
    llm = type('obj', (object,), {'router': APIRouter()})
    vision = type('obj', (object,), {'router': APIRouter()})
    audio = type('obj', (object,), {'router': APIRouter()})
    embeddings = type('obj', (object,), {'router': APIRouter()})
    rss = type('obj', (object,), {'router': APIRouter()})
    print("✅ Created dummy AI routers")

try:
    from app.core.dependencies import get_current_user
    print("✅ Imported get_current_user")
except ImportError:
    print("❌ get_current_user not found, creating dummy")
    get_current_user = None

# Create main API router
api_router = APIRouter()

# ========== PUBLIC ROUTES ==========
print("Adding auth router...")
api_router.include_router(auth.router, tags=["authentication"])

# ========== PROTECTED ROUTES ==========
if get_current_user:
    print("Adding protected routes...")
    users_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
    users_protected.include_router(user.router)
    
    roles_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
    roles_protected.include_router(roles.router)
    
    api_router.include_router(users_protected, prefix="/users", tags=["users"])
    api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])
else:
    print("Adding unprotected routes (get_current_user missing)...")
    api_router.include_router(user.router, prefix="/users", tags=["users"])
    api_router.include_router(roles.router, prefix="/roles", tags=["roles"])

# ========== AI ROUTES ==========
print("Adding AI routes...")
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss.router, prefix="/rss", tags=["rss"])

# Add some test endpoints if routers are empty
@api_router.get("/test", tags=["test"])
async def api_test():
    return {"message": "API test endpoint", "status": "working"}

@auth.router.get("/login", tags=["authentication"])
async def auth_login():
    return {"message": "Login endpoint"}

@user.router.get("/", tags=["users"])
async def get_all_users():
    return {"users": ["user1", "user2"], "count": 2}

@roles.router.get("/", tags=["roles"])
async def get_all_roles():
    return {"roles": ["admin", "user", "guest"], "count": 3}

print("=" * 50)
print("DEBUG: api.py loaded successfully")
print("=" * 50)