from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Dict, Optional, List, Any
from datetime import datetime


class EmployeeEducationBase(BaseModel):
    """Base schema for EmployeeEducation data"""
    EmployeeId: int = Field(..., description="Foreign key to Employee table")
    Degree: str = Field(..., max_length=255, description="Degree/Qualification")
    FeildOfStudy: str = Field(..., max_length=255, description="Field of study/Specialization")
    Institution: str = Field(..., max_length=500, description="Educational institution")
    YearOfCompletion: Optional[datetime] = Field(None, description="Year of completion")
    PercentageMarks: Optional[str] = Field(None, max_length=50, description="Percentage/CGPA/Marks")
    Year: str = Field(..., max_length=10, description="Year of completion")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class EmployeeEducationCreate(EmployeeEducationBase):
    """Schema for creating a new EmployeeEducation"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the education record is active")


class EmployeeEducationUpdate(BaseModel):
    """Schema for updating an existing EmployeeEducation"""
    Degree: Optional[str] = Field(None, max_length=255, description="Degree/Qualification")
    FeildOfStudy: Optional[str] = Field(None, max_length=255, description="Field of study/Specialization")
    Institution: Optional[str] = Field(None, max_length=500, description="Educational institution")
    YearOfCompletion: Optional[datetime] = Field(None, description="Year of completion")
    PercentageMarks: Optional[str] = Field(None, max_length=50, description="Percentage/CGPA/Marks")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the education record is active")
    Year: Optional[str] = Field(None, max_length=10, description="Year of completion")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class EmployeeEducationResponse(BaseModel):
    """Schema for EmployeeEducation response (read operations)"""
    EmployeeEducationId: int
    EmployeeId: int
    Degree: str
    FeildOfStudy: str
    Institution: str
    YearOfCompletion: Optional[datetime] = None
    PercentageMarks: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None
    Year: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class EmployeeEducationInDB(EmployeeEducationResponse):
    """Schema for EmployeeEducation with database-specific fields"""
    pass


class EmployeeEducationListResponse(BaseModel):
    """Schema for listing multiple EmployeeEducation records with pagination"""
    total: int
    items: List[EmployeeEducationResponse]
    page: int
    size: int
    pages: int


class EmployeeEducationExistsResponse(BaseModel):
    """Response for EmployeeEducation existence check"""
    exists: bool
    employee_education_id: Optional[int] = None


class EmployeeEducationDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee education record deleted successfully"
    employee_education_id: Optional[int] = None


class EmployeeEducationWithDetailsResponse(EmployeeEducationResponse):
    """Extended response with related data"""
    employee_name: Optional[str] = None
    completion_year: Optional[int] = Field(None, description="Extracted year from YearOfCompletion")


class EmployeeEducationCreateResponse(BaseModel):
    """Response after creating a new employee education record"""
    success: bool
    message: str = "Employee education record created successfully"
    employee_education_id: int
    education: Optional[EmployeeEducationResponse] = None


class EmployeeEducationUpdateResponse(BaseModel):
    """Response after updating an employee education record"""
    success: bool
    message: str = "Employee education record updated successfully"
    employee_education_id: int
    modified_fields: List[str] = Field(default_factory=list)
    education: Optional[EmployeeEducationResponse] = None


class EmployeeEducationBulkCreate(BaseModel):
    """Schema for creating multiple education records at once"""
    educations: List[EmployeeEducationCreate]
    employee_id: Optional[int] = None


class EmployeeEducationFilterParams(BaseModel):
    """Schema for filtering employee education records"""
    employee_id: Optional[int] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None  # Note: This is for API filter, not the actual field
    institution: Optional[str] = None
    year_from: Optional[int] = Field(None, ge=1900, le=2100, description="Completion year from")
    year_to: Optional[int] = Field(None, ge=1900, le=2100, description="Completion year to")
    is_active: Optional[bool] = None
    search_term: Optional[str] = None
    
    @field_validator('year_to')
    @classmethod
    def validate_year_range(cls, v, info):
        values = info.data
        if v is not None and values.get('year_from') is not None:
            if v < values['year_from']:
                raise ValueError('year_to must be greater than or equal to year_from')
        return v


class EmployeeEducationStatistics(BaseModel):
    """Schema for education statistics"""
    total_records: int
    degrees: Dict[str, int]
    institutions: Dict[str, int]
    by_year: Dict[int, int]