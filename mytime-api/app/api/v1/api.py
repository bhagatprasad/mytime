# app/api/v1/api.py
from fastapi import APIRouter, Depends

from app.api.v1.routers import (
    llm, vision, audio, embeddings, rss, roles, user, auth
)
from app.core.dependencies import get_current_user

# Create main API router WITHOUT global dependencies
api_router = APIRouter()

# ========== PUBLIC ROUTERS (No Authorization Required) ==========
# Auth router - must be public for login
# Note: auth.router should NOT have its own prefix if we're adding it here
api_router.include_router(
    auth.router,
    tags=["authentication"]
)  # No prefix here - endpoints will be at /api/v1/auth/...

# ========== PROTECTED ROUTERS (Authorization Required) ==========

# Create protected versions of routers
from fastapi import APIRouter as FastAPIRouter

# IMPORTANT: Ensure routers don't have their own prefixes
# If they do, remove them or adjust accordingly

# Users router - protected
users_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
users_protected.include_router(user.router)

# Roles router - protected
roles_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
roles_protected.include_router(roles.router)

# LLM router - protected (if you enable later)
# llm_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
# llm_protected.include_router(llm.router)

# Include protected routers with their prefixes
api_router.include_router(users_protected, prefix="/users", tags=["users"])
api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])

# For routers that don't need protection yet, include directly
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss.router, prefix="/rss", tags=["rss"])