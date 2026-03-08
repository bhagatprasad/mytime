from app.core.config import settings
from app.models.llm_providers import OpenAILLM, MockLLM

class ModelFactory:
    """Factory for creating model instances"""
    
    @staticmethod
    def get_llm():
        """Get LLM instance based on configuration"""
        if settings.DEFAULT_LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return OpenAILLM()
        else:
            # Fallback to mock if no API key or different provider
            return MockLLM()