from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import json

from app.schemas.user_profile_image_schema import (
    UserProfileImageResponse,
    UserProfileImageCreate,
    UserProfileImageUpdate,
    UserProfileImageListResponse,
    UserProfileImageOperationResponse,
    FileInfoSchema
)
from app.core.database import get_db
from app.services.user_profile_image_service import UserProfileImageService

router = APIRouter()

@router.get("/fetchProfileImage/{profile_image_id}", response_model=UserProfileImageResponse)
async def fetch_profile_image(profile_image_id: int, db: Session = Depends(get_db)):
    """Get profile image by ID"""
    try:
        profile_image = UserProfileImageService.fetch_profile_image(db, profile_image_id)
        if not profile_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile image with ID {profile_image_id} not found"
            )
        return profile_image
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile image: {str(e)}"
        )

@router.get("/fetchProfileImageByUser/{user_id}", response_model=UserProfileImageResponse)
async def fetch_profile_image_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get profile image by User ID"""
    try:
        profile_image = UserProfileImageService.fetch_profile_image_by_user(db, user_id)
        if not profile_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile image for user ID {user_id} not found"
            )
        return profile_image
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile image by user: {str(e)}"
        )

@router.get("/fetchAllProfileImages", response_model=List[UserProfileImageResponse])
async def fetch_all_profile_images(db: Session = Depends(get_db)):
    """Get all profile images"""
    try:
        profile_images = UserProfileImageService.fetch_all_profile_images(db)
        return profile_images
    except Exception as e:
        print(f"Error fetching profile images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile images: {str(e)}"
        )

@router.get("/getProfileImagesWithPagination", response_model=UserProfileImageListResponse)
async def get_profile_images_with_pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("Id"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """Get paginated profile images with filtering and sorting"""
    try:
        items, total = UserProfileImageService.fetch_profile_images_with_pagination(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            user_id=user_id,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching paginated profile images: {str(e)}"
        )

@router.post("/InsertOrUpdateProfileImage", response_model=UserProfileImageOperationResponse)
async def insert_or_update_profile_image(profile_image: dict, db: Session = Depends(get_db)):
    """Insert or update profile image - matches C# InsertOrUpdate pattern"""
    try:
        # Handle FileInfo if it's a string
        if 'FileInfo' in profile_image and isinstance(profile_image['FileInfo'], str):
            try:
                profile_image['FileInfo'] = json.loads(profile_image['FileInfo'])
            except:
                pass  # Keep as string if not valid JSON
                
        response = UserProfileImageService.insert_or_update_profile_image(db, profile_image)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving profile image: {str(e)}"
        )

@router.post("/uploadProfileImage", response_model=UserProfileImageOperationResponse)
async def upload_profile_image(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    created_by: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a profile image file"""
    try:
        # Read file content
        file_content = await file.read()
        content_length = len(file_content)
        
        # Here you would typically upload to cloud storage (S3, Backblaze, etc.)
        # and get back FileInfo with download URL
        
        # For now, create a placeholder FileInfo
        file_info = {
            "fileName": file.filename,
            "contentType": file.content_type,
            "contentLength": content_length,
            "storedFileName": f"user_{user_id}_{file.filename}",
            "uploadTimestamp": str(db.bind.dialect.default_now())  # Example
        }
        
        profile_image_data = {
            "UserId": user_id,
            "FileName": file.filename,
            "ContentType": file.content_type,
            "ContentLength": content_length,
            "FileInfo": file_info,
            "UploadTimestamp": db.bind.dialect.default_now(),
            "CreatedBy": created_by,
            "ModifiedBy": created_by,
            "IsActive": True
        }
        
        response = UserProfileImageService.insert_or_update_profile_image(db, profile_image_data)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading profile image: {str(e)}"
        )

@router.delete("/DeleteProfileImage/{profile_image_id}", response_model=UserProfileImageOperationResponse)
async def delete_profile_image(profile_image_id: int, db: Session = Depends(get_db)):
    """Delete profile image (hard delete)"""
    try:
        response = UserProfileImageService.delete_profile_image(db, profile_image_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting profile image: {str(e)}"
        )

@router.put("/SoftDeleteProfileImage/{profile_image_id}", response_model=UserProfileImageOperationResponse)
async def soft_delete_profile_image(
    profile_image_id: int, 
    modified_by: int = Query(...),
    db: Session = Depends(get_db)
):
    """Soft delete profile image (set IsActive = False)"""
    try:
        response = UserProfileImageService.soft_delete_profile_image(db, profile_image_id, modified_by)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating profile image: {str(e)}"
        )

@router.get("/getUserProfileImageUrl/{user_id}")
async def get_user_profile_image_url(user_id: int, db: Session = Depends(get_db)):
    """Get profile image URL for a user"""
    try:
        url = UserProfileImageService.get_user_profile_image_url(db, user_id)
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile image URL for user ID {user_id} not found"
            )
        return {"user_id": user_id, "image_url": url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile image URL: {str(e)}"
        )

@router.post("/checkUserHasActiveImage/{user_id}")
async def check_user_has_active_image(
    user_id: int, 
    exclude_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Check if user already has an active profile image"""
    try:
        has_image = UserProfileImageService.check_user_has_active_image(db, user_id, exclude_id)
        return {
            "user_id": user_id, 
            "has_active_image": has_image,
            "message": "User has active profile image" if has_image else "User has no active profile image"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking user active image: {str(e)}"
        )