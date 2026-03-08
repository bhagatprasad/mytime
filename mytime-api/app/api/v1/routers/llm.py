from fastapi import APIRouter, HTTPException, status
from app.schemas.llm_schemas import LLMRequest, LLMResponse
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/chat", response_model=LLMResponse)
async def chat(request: LLMRequest):
    """Chat with LLM"""
    try:
        service = LLMService()
        response = await service.generate(request.prompt)
        return LLMResponse(
            response=response,
            model="gpt-3.5-turbo",
            tokens_used=len(response.split())
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM error: {str(e)}"
        )

@router.post("/generate")
async def generate_text(prompt: str):
    """Generate text from prompt"""
    service = LLMService()
    response = await service.generate(prompt)
    return {"response": response}

@router.get("/health")
async def llm_health():
    """Check LLM service health"""
    return {"status": "healthy", "service": "LLM"}