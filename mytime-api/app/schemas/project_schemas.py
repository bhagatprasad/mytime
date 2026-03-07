from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProjectBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    IsActive: Optional[bool] = True

class ProjectCreate(ProjectBase):
    CreatedBy: Optional[int] = None

class ProjectUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = None

class ProjectResponse(ProjectBase):
    ProjectId: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    """Schema for listing multiple projects - matching C# return structure"""
    total: int
    items: List[ProjectResponse]
    page: int
    size: int
    pages: int

class ProjectExistsResponse(BaseModel):
    """Response for project existence check"""
    exists: bool

class ProjectDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "project deleted successfully"