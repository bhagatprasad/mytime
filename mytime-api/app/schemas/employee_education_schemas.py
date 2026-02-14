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
    ModifiedBy: Optional[int] = Field(None, description="User ID who modified the record")
    IsActive: Optional[bool] = Field(True, description="Whether the education record is active")
    CreatedOn: Optional[datetime] = Field(None, description="Creation timestamp")
    ModifiedOn: Optional[datetime] = Field(None, description="Last modification timestamp")
    EmployeeEducationId: Optional[int] = Field(0, description="Education ID (0 for new records)")
    
    @field_validator('CreatedOn', 'ModifiedOn', 'YearOfCompletion', mode='before')
    @classmethod
    def parse_datetime(cls, value):
        """Convert string dates to datetime objects"""
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Handle ISO format with Z
                if value.endswith('Z'):
                    value = value.replace('Z', '+00:00')
                return datetime.fromisoformat(value)
            except (ValueError, TypeError):
                # If parsing fails, return current time for required fields
                return datetime.utcnow()
        return value
    
    @field_validator('CreatedBy', 'ModifiedBy', 'EmployeeId', 'EmployeeEducationId', mode='before')
    @classmethod
    def parse_int(cls, value):
        """Convert string numbers to integers"""
        if value is None:
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip()) if value.strip() else None
            except (ValueError, TypeError):
                return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    @field_validator('IsActive', mode='before')
    @classmethod
    def parse_bool(cls, value):
        """Convert string booleans to boolean"""
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 't')
        if isinstance(value, int):
            return bool(value)
        return value


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
    ModifiedOn: Optional[datetime] = Field(None, description="Last modification timestamp")

    @field_validator('YearOfCompletion', 'ModifiedOn', mode='before')
    @classmethod
    def parse_update_datetime(cls, value):
        """Convert string dates to datetime objects for updates"""
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                if value.endswith('Z'):
                    value = value.replace('Z', '+00:00')
                return datetime.fromisoformat(value)
            except (ValueError, TypeError):
                return None
        return value
    
    @field_validator('ModifiedBy', mode='before')
    @classmethod
    def parse_update_int(cls, value):
        """Convert string numbers to integers for updates"""
        if value is None:
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip()) if value.strip() else None
            except (ValueError, TypeError):
                return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    @field_validator('IsActive', mode='before')
    @classmethod
    def parse_update_bool(cls, value):
        """Convert string booleans to boolean for updates"""
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 't')
        if isinstance(value, int):
            return bool(value)
        return value

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
    
    @field_validator('employee_id', mode='before')
    @classmethod
    def parse_employee_id(cls, value):
        """Convert string employee_id to integer"""
        if value is None:
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip()) if value.strip() else None
            except (ValueError, TypeError):
                return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None


class EmployeeEducationFilterParams(BaseModel):
    """Schema for filtering employee education records"""
    employee_id: Optional[int] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
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
    
    @field_validator('employee_id', mode='before')
    @classmethod
    def parse_filter_int(cls, value):
        """Convert string IDs to integers for filters"""
        if value is None:
            return value
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.strip()) if value.strip() else None
            except (ValueError, TypeError):
                return None
        return value
    
    @field_validator('is_active', mode='before')
    @classmethod
    def parse_filter_bool(cls, value):
        """Convert string booleans to boolean for filters"""
        if value is None:
            return value
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 't')
        if isinstance(value, int):
            return bool(value)
        return value


class EmployeeEducationStatistics(BaseModel):
    """Schema for education statistics"""
    total_records: int
    degrees: Dict[str, int]
    institutions: Dict[str, int]
    by_year: Dict[int, int]