from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    employee_id: Optional[int] = None
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = True


class RegisterUser(UserBase):
    id: Optional[int] = 0
    password: Optional[str] = None
    created_by: Optional[int] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    modified_by: Optional[int] = None


class UserResponse(UserBase):
    id: int
    created_by: Optional[int] = None
    created_on: Optional[datetime] = None
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    total: int
    items: List[UserResponse]
    page: int
    size: int
    pages: int


class UserExistsResponse(BaseModel):
    exists: bool


class UserDeleteResponse(BaseModel):
    success: bool
    message: str = "User deleted successfully"
