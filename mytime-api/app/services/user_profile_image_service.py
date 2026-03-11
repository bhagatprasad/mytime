from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
import json

from app.models.user_profile_image import UserProfileImage
from app.schemas.user_profile_image_schema import UserProfileImageCreate, UserProfileImageUpdate


class UserProfileImageService:

    @staticmethod
    def _serialize_file_info(data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert FileInfo dict → JSON string"""
        if "FileInfo" in data and isinstance(data["FileInfo"], dict):
            data["FileInfo"] = json.dumps(data["FileInfo"])
        return data

    @staticmethod
    def _deserialize_file_info(profile_image: UserProfileImage):
        """Convert FileInfo JSON string → dict"""
        if profile_image and profile_image.FileInfo and isinstance(profile_image.FileInfo, str):
            try:
                profile_image.FileInfo = json.loads(profile_image.FileInfo)
            except:
                pass
        return profile_image

    # -----------------------------------------

    @staticmethod
    def fetch_profile_image(db: Session, profile_image_id: int) -> Optional[UserProfileImage]:
        profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.Id == profile_image_id
        ).first()

        return UserProfileImageService._deserialize_file_info(profile_image)

    # -----------------------------------------

    @staticmethod
    def fetch_profile_image_by_user(db: Session, user_id: int) -> Optional[UserProfileImage]:
        profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        ).first()

        return UserProfileImageService._deserialize_file_info(profile_image)

    # -----------------------------------------

    @staticmethod
    def fetch_all_profile_images(db: Session):
        images = db.query(UserProfileImage).all()
        return [UserProfileImageService._deserialize_file_info(i) for i in images]

    # -----------------------------------------

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

        query = db.query(UserProfileImage)

        if user_id is not None:
            query = query.filter(UserProfileImage.UserId == user_id)

        if is_active is not None:
            query = query.filter(UserProfileImage.IsActive == is_active)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(UserProfileImage.FileName, '').ilike(search_term),
                    func.coalesce(UserProfileImage.FileId, '').ilike(search_term)
                )
            )

        total = query.count()

        sort_column = getattr(UserProfileImage, sort_by, UserProfileImage.Id)

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        items = query.offset(skip).limit(limit).all()

        items = [UserProfileImageService._deserialize_file_info(i) for i in items]

        return items, total

    # -----------------------------------------

    @staticmethod
    def insert_or_update_profile_image(db: Session, profile_image_data: dict) -> Dict[str, Any]:

        profile_image_data = UserProfileImageService._serialize_file_info(profile_image_data)

        profile_image_id = profile_image_data.get("Id")

        # UPDATE
        if profile_image_id:

            db_profile_image = db.query(UserProfileImage).filter(
                UserProfileImage.Id == profile_image_id
            ).first()

            if not db_profile_image:
                return {
                    "success": False,
                    "message": "Profile image not found",
                    "profile_image": None
                }

            user_id = profile_image_data.get("UserId")

            if user_id and user_id != db_profile_image.UserId:
                if UserProfileImageService.check_user_has_active_image(db, user_id, profile_image_id):
                    return {
                        "success": False,
                        "message": "User already has an active profile image",
                        "profile_image": None
                    }

            for key, value in profile_image_data.items():
                if key != "Id" and value is not None:
                    setattr(db_profile_image, key, value)

            db.commit()
            db.refresh(db_profile_image)

            db_profile_image = UserProfileImageService._deserialize_file_info(db_profile_image)

            return {
                "success": True,
                "message": "Profile image updated successfully",
                "profile_image": db_profile_image
            }

        # INSERT
        else:

            user_id = profile_image_data.get("UserId")

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

            db_profile_image = UserProfileImageService._deserialize_file_info(db_profile_image)

            return {
                "success": True,
                "message": "Profile image created successfully",
                "profile_image": db_profile_image
            }

    # -----------------------------------------

    @staticmethod
    def delete_profile_image(db: Session, profile_image_id: int) -> Dict[str, Any]:

        db_profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.Id == profile_image_id
        ).first()

        if not db_profile_image:
            return {"success": False, "message": "Profile image not found"}

        db.delete(db_profile_image)
        db.commit()

        return {"success": True, "message": "Profile image deleted successfully"}

    # -----------------------------------------

    @staticmethod
    def soft_delete_profile_image(db: Session, profile_image_id: int, modified_by: int) -> Dict[str, Any]:

        db_profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.Id == profile_image_id
        ).first()

        if not db_profile_image:
            return {"success": False, "message": "Profile image not found"}

        db_profile_image.IsActive = False
        db_profile_image.ModifiedBy = modified_by
        db_profile_image.ModifiedOn = func.now()

        db.commit()
        db.refresh(db_profile_image)

        return {
            "success": True,
            "message": "Profile image deactivated successfully",
            "profile_image": db_profile_image
        }

    # -----------------------------------------

    @staticmethod
    def check_user_has_active_image(db: Session, user_id: int, exclude_id: Optional[int] = None) -> bool:

        query = db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        )

        if exclude_id:
            query = query.filter(UserProfileImage.Id != exclude_id)

        return query.first() is not None

    # -----------------------------------------

    @staticmethod
    def get_user_profile_image_url(db: Session, user_id: int) -> Optional[str]:

        profile_image = db.query(UserProfileImage).filter(
            UserProfileImage.UserId == user_id,
            UserProfileImage.IsActive == True
        ).first()

        profile_image = UserProfileImageService._deserialize_file_info(profile_image)

        if profile_image and profile_image.FileInfo:
            return profile_image.FileInfo.get("downloadUrl")

        return None