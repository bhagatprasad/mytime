from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass