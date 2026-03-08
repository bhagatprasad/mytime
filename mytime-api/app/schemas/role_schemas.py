from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=100)
    IsActive: Optional[bool] = True

class RoleCreate(RoleBase):
    CreatedBy: Optional[int] = None

class RoleUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=100)
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = None

class RoleResponse(RoleBase):
    Id: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RoleListResponse(BaseModel):
    """Schema for listing multiple roles - matching C# return structure"""
    total: int
    items: List[RoleResponse]
    page: int
    size: int
    pages: int

class RoleExistsResponse(BaseModel):
    """Response for role existence check"""
    exists: bool

class RoleDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Role deleted successfully"