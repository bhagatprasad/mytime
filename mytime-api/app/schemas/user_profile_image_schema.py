from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

# Base UserProfileImage Schema
class UserProfileImageBase(BaseModel):
    UserId: Optional[int] = None
    FileId: Optional[str] = None
    FileName: Optional[str] = None
    BucketId: Optional[str] = None
    ContentLength: Optional[int] = None
    ContentType: Optional[str] = None
    FileInfo: Optional[Dict[str, Any]] = None  # For JSON data
    UploadTimestamp: Optional[datetime] = None
    IsActive: Optional[bool] = True

# Schema for creating a user profile image
class UserProfileImageCreate(UserProfileImageBase):
    UserId: int  # Make UserId required for creation
    FileId: str  # Make FileId required
    FileName: str  # Make FileName required
    ContentType: str  # Make ContentType required
    CreatedBy: Optional[int] = None
    ModifiedBy: Optional[int] = None

# Schema for updating a user profile image
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

# Schema for user profile image in database (response)
class UserProfileImageInDB(UserProfileImageBase):
    Id: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema for user profile image response
class UserProfileImageResponse(UserProfileImageInDB):
    pass

# Schema for user profile image list response with pagination
class UserProfileImageListResponse(BaseModel):
    items: list[UserProfileImageResponse]
    total: int
    skip: int
    limit: int

# Schema for user profile image operation response
class UserProfileImageOperationResponse(BaseModel):
    success: bool
    message: str
    profile_image: Optional[UserProfileImageResponse] = None

# Schema for uploading image (if handling file uploads)
class UserProfileImageUpload(BaseModel):
    UserId: int
    FileName: str
    ContentType: str
    ContentLength: int
    CreatedBy: Optional[int] = None

# Schema for FileInfo structure (example)
class FileInfoSchema(BaseModel):
    downloadUrl: Optional[str] = None
    storedFileName: Optional[str] = None
    bucketName: Optional[str] = None
    etag: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)