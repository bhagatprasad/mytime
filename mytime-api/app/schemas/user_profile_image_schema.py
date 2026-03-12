from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class FileInfoSchema(BaseModel):
    downloadUrl: Optional[str] = None
    storedFileName: Optional[str] = None
    bucketName: Optional[str] = None
    etag: Optional[str] = None


class UserProfileImageBase(BaseModel):
    UserId: Optional[int] = None
    FileId: Optional[str] = None
    FileName: Optional[str] = None
    BucketId: Optional[str] = None
    ContentLength: Optional[int] = None
    ContentType: Optional[str] = None

    # Accept dict in API
    FileInfo: Optional[Dict[str, Any]] = None

    UploadTimestamp: Optional[datetime] = None
    IsActive: Optional[bool] = True


class UserProfileImageCreate(UserProfileImageBase):
    UserId: int
    FileId: str
    FileName: str
    ContentType: str
    CreatedBy: Optional[int] = None
    ModifiedBy: Optional[int] = None


class UserProfileImageUpdate(BaseModel):
    UserId: Optional[int] = None
    FileId: Optional[str] = None
    FileName: Optional[str] = None
    BucketId: Optional[str] = None
    ContentLength: Optional[int] = None
    ContentType: Optional[str] = None
    FileInfo: Optional[Dict[str, Any]] = None
    UploadTimestamp: Optional[datetime] = None
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = None


class UserProfileImageInDB(UserProfileImageBase):
    Id: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserProfileImageResponse(UserProfileImageInDB):
    pass


class UserProfileImageListResponse(BaseModel):
    items: list[UserProfileImageResponse]
    total: int
    skip: int
    limit: int


class UserProfileImageOperationResponse(BaseModel):
    success: bool
    message: str
    profile_image: Optional[UserProfileImageResponse] = None