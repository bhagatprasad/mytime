from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# 🔹 Base Schema
class EmployeeDocumentBase(BaseModel):
    """Base schema for EmployeeDocument data"""

    EmployeeId: Optional[int] = Field(None, description="Associated employee ID")
    DocumentType: Optional[str] = Field(None, max_length=255, description="Type of document")

    FileId: Optional[str] = Field(None, max_length=255, description="Storage file ID")
    FileName: Optional[str] = Field(None, max_length=500, description="Uploaded file name")
    BucketId: Optional[str] = Field(None, max_length=255, description="Storage bucket ID")

    ContentLength: Optional[int] = Field(None, ge=0, description="File size in bytes")
    ContentType: Optional[str] = Field(None, max_length=255, description="MIME content type")
    FileInfo: Optional[str] = Field(None, description="Additional file metadata (JSON)")
    UploadTimestamp: Optional[datetime] = Field(None, description="File upload timestamp")


# 🔹 Create Schema
class EmployeeDocumentCreate(EmployeeDocumentBase):
    """Schema for creating a new EmployeeDocument"""

    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the document is active")


# 🔹 Update Schema
class EmployeeDocumentUpdate(BaseModel):
    """Schema for updating an existing EmployeeDocument"""

    DocumentType: Optional[str] = Field(None, max_length=255)
    FileId: Optional[str] = Field(None, max_length=255)
    FileName: Optional[str] = Field(None, max_length=500)
    BucketId: Optional[str] = Field(None, max_length=255)

    ContentLength: Optional[int] = Field(None, ge=0)
    ContentType: Optional[str] = Field(None, max_length=255)
    FileInfo: Optional[str] = Field(None)
    UploadTimestamp: Optional[datetime] = Field(None)

    ModifiedBy: Optional[int] = Field(None)
    IsActive: Optional[bool] = Field(None)


# 🔹 Response Schema
class EmployeeDocumentResponse(BaseModel):
    """Schema for EmployeeDocument response (read operations)"""

    EmployeeDocumentId: int
    EmployeeId: Optional[int] = None

    DocumentType: Optional[str] = None

    FileId: Optional[str] = None
    FileName: Optional[str] = None
    BucketId: Optional[str] = None

    ContentLength: Optional[int] = None
    ContentType: Optional[str] = None
    FileInfo: Optional[str] = None
    UploadTimestamp: Optional[datetime] = None

    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# 🔹 List Response (Pagination)
class EmployeeDocumentListResponse(BaseModel):
    """Schema for listing EmployeeDocuments with pagination"""

    total: int
    items: List[EmployeeDocumentResponse]
    page: int
    size: int
    pages: int


# 🔹 Exists Response
class EmployeeDocumentExistsResponse(BaseModel):
    """Response for existence check"""

    exists: bool
    employee_document_id: Optional[int] = None


# 🔹 Delete Response
class EmployeeDocumentDeleteResponse(BaseModel):
    """Response for delete operation"""

    success: bool
    message: str = "Employee document deleted successfully"
    employee_document_id: Optional[int] = None


# 🔹 Create Response
class EmployeeDocumentCreateResponse(BaseModel):
    """Response after creating document"""

    success: bool
    message: str = "Employee document created successfully"
    employee_document_id: int


# 🔹 Update Response
class EmployeeDocumentUpdateResponse(BaseModel):
    """Response after updating document"""

    success: bool
    message: str = "Employee document updated successfully"
    employee_document_id: int
    modified_fields: List[str] = Field(default_factory=list)


# 🔹 Filter Parameters
class EmployeeDocumentFilterParams(BaseModel):
    """Schema for filtering documents"""

    employee_id: Optional[int] = None
    document_type: Optional[str] = None
    is_active: Optional[bool] = None
    search_term: Optional[str] = None
