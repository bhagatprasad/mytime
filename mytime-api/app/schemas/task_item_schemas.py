from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class TaskItemBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=50)
    IsActive: Optional[bool] = Field(True)

class TaskItemCreate(TaskItemBase):
    CreatedBy: Optional[int] = Field(None)
    ProjectId: Optional[int] = Field(None)

class TaskItemUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=50)
    ModifiedBy: Optional[int] = Field(None)
    IsActive: Optional[bool] = Field(None)
    ProjectId: Optional[int] = Field(None)
    
class TaskItemResponse(BaseModel):
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
    total: int
    items: List[TaskItemResponse]
    page: int
    size: int
    pages: int

class TaskItemExistsResponse(BaseModel):
    exists: bool

class TaskItemDeleteResponse(BaseModel):
    success: bool
    message: str = "TaskItem deleted successfully"