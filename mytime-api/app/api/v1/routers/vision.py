from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.vision_service import VisionService

router = APIRouter(prefix="/vision", tags=["Vision"])

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Save file temporarily
        contents = await file.read()
        with open(f"temp_{file.filename}", "wb") as f:
            f.write(contents)
        
        # Analyze image
        service = VisionService()
        result = await service.analyze(f"temp_{file.filename}")
        
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from image"""
    service = VisionService()
    result = await service.extract_text("placeholder_path")
    return {"text": result}