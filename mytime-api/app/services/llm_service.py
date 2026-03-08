from app.services.model_factory import ModelFactory
from app.services.cache_service import CacheService
from app.core.config import settings

class LLMService:
    """Service for LLM operations"""
    
    def __init__(self):
        self.llm = ModelFactory.get_llm()
    
    async def generate(self, prompt: str) -> str:
        """Generate response for prompt with caching"""
        # Check cache first
        cache_key = f"llm:{hash(prompt)}"
        if settings.ENABLE_CACHE:
            cached = CacheService.get(cache_key)
            if cached:
                return cached
        
        # Generate response
        response = await self.llm.generate(prompt)
        
        # Cache the response
        if settings.ENABLE_CACHE:
            CacheService.set(cache_key, response, ttl=settings.CACHE_TTL)
        
        return response