from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class TaskcodeBase(BaseModel):
    TaskItemId: Optional[int] = Field(None)
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=255)

class TaskcodeCreate(TaskcodeBase):
    CreatedBy: Optional[int] = Field(None)
    IsActive: Optional[bool] = Field(True)

class TaskcodeUpdate(BaseModel):
    TaskCodeId: Optional[int] = Field(None)
    TaskItemId: Optional[int] = Field(None)
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=255)
    ModifiedBy: Optional[int] = Field(None)
    IsActive: Optional[bool] = Field(None)

class TaskcodeResponse(BaseModel):
    TaskCodeId: int
    Name: Optional[str] = None
    Code: Optional[str] = None
    TaskItemId: Optional[int] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    total: int
    items: List[TaskcodeResponse]
    page: int
    size: int
    pages: int

class TaskcodeExistResponse(BaseModel):
    exists: bool

class TaskcodeDeleteResponse(BaseModel):
    success: bool
    message: str = "Taskcode deleted successfully"