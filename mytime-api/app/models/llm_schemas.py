from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(2000, ge=1, le=4000)

class LLMResponse(BaseModel):
    response: str
    model: str
    tokens_used: int = 0