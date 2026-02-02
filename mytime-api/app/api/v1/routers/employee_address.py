from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.employee_address_schemas import (
    EmployeeAddressCreate, EmployeeAddressUpdate, EmployeeAddressResponse,
    EmployeeAddressListResponse, EmployeeAddressExistsResponse,
    EmployeeAddressDeleteResponse, EmployeeAddressCreateResponse,
    EmployeeAddressUpdateResponse, EmployeeAddressBulkCreate,
    EmployeeAddressFilterParams, EmployeeAddressWithDetailsResponse
)
from app.core.database import get_db
from app.services.employee_address_service import EmployeeAddressService

router = APIRouter(prefix="/employee-addresses", tags=["employee-addresses"])


@router.get("/fetchEmployeeAddress/{employee_address_id}", response_model=EmployeeAddressResponse)
async def fetch_employee_address(employee_address_id: int, db: Session = Depends(get_db)):
    """Get employee address by ID"""
    try:
        address = EmployeeAddressService.fetch_employee_address(db, employee_address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee address with ID {employee_address_id} not found"
            )
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee address: {str(e)}"
        )


@router.get("/fetchAddressesByEmployee/{employee_id}", response_model=List[EmployeeAddressResponse])
async def fetch_addresses_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all addresses for a specific employee"""
    try:
        addresses = EmployeeAddressService.fetch_addresses_by_employee(db, employee_id)
        return addresses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching addresses for employee: {str(e)}"
        )


@router.get("/fetchActiveAddressesByEmployee/{employee_id}", response_model=List[EmployeeAddressResponse])
async def fetch_active_addresses_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get active addresses for a specific employee"""
    try:
        addresses = EmployeeAddressService.fetch_active_addresses_by_employee(db, employee_id)
        return addresses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active addresses for employee: {str(e)}"
        )


@router.get("/fetchAllEmployeeAddresses", response_model=List[EmployeeAddressResponse])
async def fetch_all_employee_addresses(db: Session = Depends(get_db)):
    """Get all employee addresses"""
    try:
        addresses = EmployeeAddressService.fetch_all_employee_addresses(db)
        return addresses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee addresses: {str(e)}"
        )


@router.get("/getEmployeeAddresses", response_model=EmployeeAddressListResponse)
async def get_employee_addresses(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    city_id: Optional[int] = Query(None, description="Filter by city ID"),
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("EmployeeAddressId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee addresses with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeAddressService.get_employee_addresses_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            city_id=city_id,
            state_id=state_id,
            country_id=country_id,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size  # Ceiling division
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee addresses: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeAddress")
async def insert_or_update_employee_address(address: dict, db: Session = Depends(get_db)):
    """Insert or update employee address"""
    try:
        response = EmployeeAddressService.insert_or_update_employee_address(db, address)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving employee address: {str(e)}"
        )


@router.delete("/DeleteEmployeeAddress/{employee_address_id}", response_model=EmployeeAddressDeleteResponse)
async def delete_employee_address(employee_address_id: int, db: Session = Depends(get_db)):
    """Delete employee address"""
    try:
        response = EmployeeAddressService.delete_employee_address(db, employee_address_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting employee address: {str(e)}"
        )


@router.patch("/SoftDeleteEmployeeAddress/{employee_address_id}", response_model=EmployeeAddressResponse)
async def soft_delete_employee_address(
    employee_address_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee address (deactivate)"""
    try:
        response = EmployeeAddressService.soft_delete_employee_address(
            db, employee_address_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["address"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee address: {str(e)}"
        )


@router.get("/checkEmployeeAddressExists", response_model=EmployeeAddressExistsResponse)
async def check_employee_address_exists(
    employee_id: int = Query(..., description="Employee ID"),
    address_line_one: str = Query(..., description="Address line 1"),
    db: Session = Depends(get_db)
):
    """Check if address exists for employee"""
    try:
        result = EmployeeAddressService.check_address_exists(db, employee_id, address_line_one)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee address existence: {str(e)}"
        )


@router.patch("/setPrimaryAddress/{employee_address_id}", response_model=EmployeeAddressResponse)
async def set_primary_address(
    employee_address_id: int,
    employee_id: int = Query(..., description="Employee ID"),
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Set an address as primary (deactivate others)"""
    try:
        response = EmployeeAddressService.set_primary_address(
            db, employee_id, employee_address_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response["address"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting primary address: {str(e)}"
        )


@router.post("/createBulkAddresses", response_model=List[EmployeeAddressResponse])
async def create_bulk_addresses(
    bulk_data: EmployeeAddressBulkCreate,
    db: Session = Depends(get_db)
):
    """Create multiple addresses at once"""
    try:
        addresses = EmployeeAddressService.create_bulk_addresses(
            db, bulk_data.addresses, bulk_data.employee_id
        )
        return addresses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bulk addresses: {str(e)}"
        )


# Alternative endpoints using Pydantic models
@router.post("/create", response_model=EmployeeAddressCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_address(
    address: EmployeeAddressCreate, 
    db: Session = Depends(get_db)
):
    """Create a new employee address using Pydantic model"""
    try:
        # Check if address already exists for this employee
        exists_result = EmployeeAddressService.check_address_exists(
            db, address.EmployeeId, address.AddressLineOne
        )
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Address already exists for this employee (ID: {exists_result['employee_address_id']})"
            )
        
        db_address = EmployeeAddressService.create_employee_address(db, address)
        return {
            "success": True,
            "message": "Employee address created successfully",
            "employee_address_id": db_address.EmployeeAddressId
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee address: {str(e)}"
        )


@router.put("/update/{employee_address_id}", response_model=EmployeeAddressUpdateResponse)
async def update_employee_address(
    employee_address_id: int, 
    address: EmployeeAddressUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing employee address using Pydantic model"""
    try:
        updated_address = EmployeeAddressService.update_employee_address(
            db, employee_address_id, address
        )
        if not updated_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee address with ID {employee_address_id} not found"
            )
        
        # Get list of updated fields
        updated_fields = list(address.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee address updated successfully",
            "employee_address_id": employee_address_id,
            "modified_fields": updated_fields
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating employee address: {str(e)}"
        )


@router.get("/getPrimaryAddress/{employee_id}", response_model=Optional[EmployeeAddressResponse])
async def get_primary_address(employee_id: int, db: Session = Depends(get_db)):
    """Get primary (active) address for an employee"""
    try:
        addresses = EmployeeAddressService.fetch_active_addresses_by_employee(db, employee_id)
        if addresses:
            return addresses[0]  # Return first active address
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching primary address: {str(e)}"
        )


@router.post("/searchEmployeeAddresses", response_model=EmployeeAddressListResponse)
async def search_employee_addresses(
    filters: EmployeeAddressFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeAddressId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee address search with filters"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeAddressService.get_employee_addresses_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term,
            employee_id=filters.employee_id,
            city_id=filters.city_id,
            state_id=filters.state_id,
            country_id=filters.country_id,
            is_active=filters.is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching employee addresses: {str(e)}"
        )