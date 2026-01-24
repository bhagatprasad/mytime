# app/api/v1/routers/__init__.py
from .auth import router as auth_router
from .user import router as user_router
from .roles import router as roles_router
from .llm import router as llm_router
from .vision import router as vision_router
from .audio import router as audio_router
from .embeddings import router as embeddings_router
from .rss import router as rss_router

# OR if you want to import the modules directly:
from . import auth, user, roles, llm, vision, audio, embeddings, rss

__all__ = ["auth", "user", "roles", "llm", "vision", "audio", "embeddings", "rss"]
