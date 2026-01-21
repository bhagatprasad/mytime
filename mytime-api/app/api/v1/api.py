from fastapi import APIRouter
from app.api.v1.routers import (
    llm, vision, audio, embeddings, rss, roles,user,auth
)

api_router = APIRouter()

# Include all routers
api_router.include_router(llm.router)
api_router.include_router(vision.router)
api_router.include_router(audio.router)
api_router.include_router(embeddings.router)
api_router.include_router(rss.router)
api_router.include_router(roles.router)
api_router.include_router(user.router)
api_router.include_router(auth.router)