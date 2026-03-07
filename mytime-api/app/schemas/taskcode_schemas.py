from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class TaskcodeBase(BaseModel):
    """Base schema for State data"""
    TaskItemId: int = Field(..., description="Foreign key to task item table")
    Name: str = Field(..., max_length=255, description="taskcode name")
    Code: str = Field(..., max_length=255, description="taskcode code")


class TaskcodeCreate(TaskcodeBase):
    """Schema for creating a new State"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the state is active")


class TaskcodeUpdate(BaseModel):
    """Schema for updating an existing State"""
    TaskItemId: int = Field(..., description="Foreign key to task item table")
    Name: str = Field(..., max_length=255, description="taskcode name")
    Code: str = Field(..., max_length=255, description="taskcode code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the state is active")


class TaskcodeResponse(BaseModel):
    """Schema for taskcode response (read operations)"""
    TaskCodeId: int
    Name: str
    Code: str
    TaskItemId: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for listing multiple States with pagination"""
    total: int
    items: List[TaskcodeResponse]
    page: int
    size: int
    pages: int


class TaskcodeExistResponse(BaseModel):
    """Response for taskcode existence check"""
    exists: bool


class TaskcodeDeleteResponse(BaseModel):
    """Response for taskcode operation"""
    success: bool
    message: str = "taskcode deleted successfully"