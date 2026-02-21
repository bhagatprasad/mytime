from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    employee_id: Optional[int] = Field(None, alias="EmployeeId")
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    role_id: Optional[int] = Field(None, alias="RoleId")
    department_id: Optional[int] = Field(None, alias="DepartmentId")
    email: Optional[str] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    is_active: Optional[bool] = Field(True, alias="IsActive")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RegisterUser(BaseModel):
    id: Optional[int] = 0
    password: Optional[str] = None
    employee_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    created_by: Optional[int] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    role_id: Optional[int] = Field(None, alias="RoleId")
    department_id: Optional[int] = Field(None, alias="DepartmentId")
    email: Optional[str] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    is_active: Optional[bool] = Field(None, alias="IsActive")
    modified_by: Optional[int] = Field(None, alias="ModifiedBy")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserResponse(UserBase):
    id: int = Field(alias="Id")
    created_by: Optional[int] = Field(None, alias="CreatedBy")
    created_on: Optional[datetime] = Field(None, alias="CreatedOn")
    modified_by: Optional[int] = Field(None, alias="ModifiedBy")
    modified_on: Optional[datetime] = Field(None, alias="ModifiedOn")


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