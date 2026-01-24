# app/api/v1/api.py - UPDATED
from fastapi import APIRouter, Depends

# After updating __init__.py, these imports will work
from app.api.v1.routers import (
    auth_router, user_router, roles_router, llm_router, 
    vision_router, audio_router, embeddings_router, rss_router
)
from app.core.dependencies import get_current_user

api_router = APIRouter()

# Use the imported routers
api_router.include_router(auth_router, tags=["authentication"])

# ... rest of your code, but use the renamed routers:
users_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
users_protected.include_router(user_router)

roles_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
roles_protected.include_router(roles_router)

api_router.include_router(users_protected, prefix="/users", tags=["users"])
api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])

api_router.include_router(llm_router, prefix="/llm", tags=["llm"])
api_router.include_router(vision_router, prefix="/vision", tags=["vision"])
api_router.include_router(audio_router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings_router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss_router, prefix="/rss", tags=["rss"])
