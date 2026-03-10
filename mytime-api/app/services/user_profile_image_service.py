from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.user_profile_image import UserProfileImage
from app.schemas.user_profile_image_schema import UserProfileImageCreate, UserProfileImageUpdate

class UserProfileImageService:
    """Service for UserProfileImage operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_profile_image(db: Session, profile_image_id: int) -> Optional[UserProfileImage]:
        """Get profile image by ID"""
        profile_image = db.query(UserProfileImage).filter(UserProfileImage.Id == profile_image_id).first()

        if not profile_image:
            return {"message": "Profile image not found"}

        return profile_image
    
    @staticmethod
    def fetch_profile_image_by_user(db: Session, user_id: int) -> Optional[UserProfileImage]:
        """Get profile image by User ID"""
        return db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        ).first()
    
    @staticmethod
    def fetch_all_profile_images(db: Session):
        """Get all profile images"""
        return db.query(UserProfileImage).all()
    
    @staticmethod
    def fetch_profile_images_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        user_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[UserProfileImage], int]:
        """Get paginated profile images with filtering and sorting"""
        query = db.query(UserProfileImage)
        
        # Apply filters
        if user_id is not None:
            query = query.filter(UserProfileImage.UserId == user_id)
        
        if is_active is not None:
            query = query.filter(UserProfileImage.IsActive == is_active)
        
        # Apply search filter (on filename)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(UserProfileImage.FileName, '').ilike(search_term),
                    func.coalesce(UserProfileImage.FileId, '').ilike(search_term)
                )
            )
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(UserProfileImage, sort_by, UserProfileImage.Id)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_profile_image(db: Session, profile_image_data: dict) -> Dict[str, Any]:
        """Insert or update profile image"""
        profile_image_id = profile_image_data.get("Id")

        # UPDATE
        if profile_image_id:
            db_profile_image = db.query(UserProfileImage).filter(UserProfileImage.Id == profile_image_id).first()

            if not db_profile_image:
                return {
                    "success": False,
                    "message": "Profile image not found",
                    "profile_image": None
                }

            user_id = profile_image_data.get("UserId")
            file_name = profile_image_data.get("FileName")
            file_id = profile_image_data.get("FileId")

            # Check for existing active profile image for this user (if updating UserId)
            if user_id and user_id != db_profile_image.UserId:
                if UserProfileImageService.check_user_has_active_image(db, user_id, profile_image_id):
                    return {
                        "success": False,
                        "message": "User already has an active profile image",
                        "profile_image": None
                    }

            # update fields
            for key, value in profile_image_data.items():
                if key != "Id" and value is not None:
                    setattr(db_profile_image, key, value)

            db.commit()
            db.refresh(db_profile_image)

            return {
                "success": True,
                "message": "Profile image updated successfully",
                "profile_image": db_profile_image
            }

        # INSERT
        else:
            user_id = profile_image_data.get("UserId")

            # Check if user already has an active profile image
            if UserProfileImageService.check_user_has_active_image(db, user_id):
                return {
                    "success": False,
                    "message": "User already has an active profile image",
                    "profile_image": None
                }

            profile_image_data.pop("Id", None)

            db_profile_image = UserProfileImage(**profile_image_data)

            db.add(db_profile_image)
            db.commit()
            db.refresh(db_profile_image)

            return {
                "success": True,
                "message": "Profile image created successfully",
                "profile_image": db_profile_image
            }
    
    @staticmethod
    def delete_profile_image(db: Session, profile_image_id: int) -> Dict[str, Any]:
        """Delete profile image (hard delete)"""
        db_profile_image = db.query(UserProfileImage).filter(UserProfileImage.Id == profile_image_id).first()
        if not db_profile_image:
            return {"success": False, "message": "Profile image not found"}
        
        db.delete(db_profile_image)
        db.commit()
        return {"success": True, "message": "Profile image deleted successfully"}
    
    @staticmethod
    def soft_delete_profile_image(db: Session, profile_image_id: int, modified_by: int) -> Dict[str, Any]:
        """Soft delete profile image (set IsActive = False)"""
        db_profile_image = db.query(UserProfileImage).filter(UserProfileImage.Id == profile_image_id).first()
        if not db_profile_image:
            return {"success": False, "message": "Profile image not found"}
        
        db_profile_image.IsActive = False
        db_profile_image.ModifiedBy = modified_by
        db_profile_image.ModifiedOn = func.now()
        
        db.commit()
        db.refresh(db_profile_image)
        
        return {"success": True, "message": "Profile image deactivated successfully", "profile_image": db_profile_image}
    
    @staticmethod
    def check_user_has_active_image(db: Session, user_id: int, exclude_id: Optional[int] = None) -> bool:
        """Check if user already has an active profile image"""
        query = db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        )
        
        if exclude_id:
            query = query.filter(UserProfileImage.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_user_profile_image_url(db: Session, user_id: int) -> Optional[str]:
        """Get profile image URL for a user"""
        profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        ).first()
        
        if profile_image and profile_image.FileInfo:
            # Extract URL from FileInfo JSON
            file_info = profile_image.FileInfo
            if isinstance(file_info, dict):
                return file_info.get('downloadUrl')
            elif isinstance(file_info, str):
                # Try to parse if it's a JSON string
                import json
                try:
                    file_info_dict = json.loads(file_info)
                    return file_info_dict.get('downloadUrl')
                except:
                    pass
        
        return None
    
    @staticmethod
    def create_profile_image(db: Session, profile_image: UserProfileImageCreate) -> UserProfileImage:
        """Create new profile image"""
        # Check if user already has active image
        if UserProfileImageService.check_user_has_active_image(db, profile_image.UserId):
            raise ValueError("User already has an active profile image")
        
        db_profile_image = UserProfileImage(**profile_image.model_dump(exclude_none=True))
        db.add(db_profile_image)
        db.commit()
        db.refresh(db_profile_image)
        return db_profile_image
    
    @staticmethod
    def update_profile_image(db: Session, profile_image_id: int, profile_image: UserProfileImageUpdate) -> Optional[UserProfileImage]:
        """Update existing profile image"""
        db_profile_image = db.query(UserProfileImage).filter(UserProfileImage.Id == profile_image_id).first()
        if db_profile_image:
            # If updating UserId, check if target user already has active image
            if profile_image.UserId and profile_image.UserId != db_profile_image.UserId:
                if UserProfileImageService.check_user_has_active_image(db, profile_image.UserId, profile_image_id):
                    raise ValueError("Target user already has an active profile image")
            
            for key, value in profile_image.model_dump(exclude_none=True).items():
                setattr(db_profile_image, key, value)
            db.commit()
            db.refresh(db_profile_image)
        return db_profile_image