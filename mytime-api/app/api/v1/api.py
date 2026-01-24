# app/api/v1/api.py - CORRECTED
from fastapi import APIRouter, Depends

# Change back to original import style
from app.api.v1.routers import (
    auth, user, roles, llm, vision, audio, embeddings, rss
)
from app.core.dependencies import get_current_user

api_router = APIRouter()

# Use the modules (each module has a 'router' attribute)
api_router.include_router(auth.router, tags=["authentication"])

# Create protected versions
from fastapi import APIRouter as FastAPIRouter

users_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
users_protected.include_router(user.router)

roles_protected = FastAPIRouter(dependencies=[Depends(get_current_user)])
roles_protected.include_router(roles.router)

api_router.include_router(users_protected, prefix="/users", tags=["users"])
api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])

api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss.router, prefix="/rss", tags=["rss"])
