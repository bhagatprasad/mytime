from openai import AsyncOpenAI
import httpx

from app.core.config import settings
from app.models.base import BaseLLM

class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

class MockLLM(BaseLLM):
    """Mock LLM for testing"""
    
    async def generate(self, prompt: str) -> str:
        return f"Mock response to: {prompt}"