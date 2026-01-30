from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class DocumentTypeBase(BaseModel):
    """Base schema for DocumentType data"""
    Name: Optional[str] = Field(None, max_length=255, description="Document type name")
    IsActive: Optional[bool] = Field(True, description="Whether the document type is active")


class DocumentTypeCreate(DocumentTypeBase):
    """Schema for creating a new DocumentType"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class DocumentTypeUpdate(BaseModel):
    """Schema for updating an existing DocumentType"""
    Name: Optional[str] = Field(None, max_length=255, description="Document type name")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the document type is active")


class DocumentTypeResponse(BaseModel):
    """Schema for DocumentType response (read operations)"""
    Id: int
    Name: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class DocumentTypeListResponse(BaseModel):
    """Schema for listing multiple DocumentTypes with pagination"""
    total: int
    items: List[DocumentTypeResponse]
    page: int
    size: int
    pages: int


class DocumentTypeExistsResponse(BaseModel):
    """Response for DocumentType existence check"""
    exists: bool


class DocumentTypeDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Document type deleted successfully"