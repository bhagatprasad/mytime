from pydantic import BaseModel, Field, ConfigDict
from typing import Optional,List
from datetime import datetime



class TaskItemBase(BaseModel):
    """Base schema for TaskItem data"""
    Name: Optional[str] = Field(None, max_length=255, description="TaskItem name")
    Code: Optional[str] = Field(None, max_length=50, description="TaskItem code")
    IsActive: Optional[bool] = Field(True, description="Whether the TaskItem is active")

    
class TaskItemCreate(TaskItemBase):
    """Schema for creating a new TaskItem"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class TaskItemUpdate(BaseModel):
    """Schema for updating an existing TaskItem"""
    Name: Optional[str] = Field(None, max_length=255, description="TaskItem name")
    Code: Optional[str] = Field(None, max_length=50, description="TaskItem code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the TaskItem is active")  
    
class TaskItemResponse(BaseModel):
    """Schema for TaskItem response (read operations)"""
    TaskItemId: int
    Name: Optional[str] = None
    Code: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None
    ProjectId: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class TaskItemListResponse(BaseModel):
    """Schema for listing multiple TaskItem with pagination"""
    total: int
    items: List[TaskItemResponse]
    page: int
    size: int
    pages: int


class TaskItemExistsResponse(BaseModel):
    """Response for TaskItem existence check"""
    exists: bool


class TaskItemDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "TaskItem deleted successfully"
  
    
