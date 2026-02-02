from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.employee_emergency_contact import EmployeeEmergencyContact
from app.schemas.employee_emergency_contact_schemas import (
    EmployeeEmergencyContactCreate, EmployeeEmergencyContactUpdate, EmployeeEmergencyContactResponse,
    EmployeeEmergencyContactListResponse, EmployeeEmergencyContactExistsResponse,
    EmployeeEmergencyContactDeleteResponse, EmployeeEmergencyContactCreateResponse,
    EmployeeEmergencyContactUpdateResponse, EmployeeEmergencyContactBulkCreate,
    EmployeeEmergencyContactFilterParams, EmployeeEmergencyContactWithDetailsResponse
)
from app.core.database import get_db
from app.services.employee_emergency_contact_service import EmployeeEmergencyContactService

router = APIRouter()


@router.get("/fetchEmployeeEmergencyContact/{employee_emergency_contact_id}", response_model=EmployeeEmergencyContactResponse)
async def fetch_employee_emergency_contact(employee_emergency_contact_id: int, db: Session = Depends(get_db)):
    """Get employee emergency contact by ID"""
    try:
        contact = EmployeeEmergencyContactService.fetch_employee_emergency_contact(db, employee_emergency_contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee emergency contact with ID {employee_emergency_contact_id} not found"
            )
        return contact
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee emergency contact: {str(e)}"
        )


@router.get("/fetchContactsByEmployee/{employee_id}", response_model=List[EmployeeEmergencyContactResponse])
async def fetch_contacts_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all emergency contacts for a specific employee"""
    try:
        contacts = EmployeeEmergencyContactService.fetch_contacts_by_employee(db, employee_id)
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching emergency contacts for employee: {str(e)}"
        )


@router.get("/fetchActiveContactsByEmployee/{employee_id}", response_model=List[EmployeeEmergencyContactResponse])
async def fetch_active_contacts_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get active emergency contacts for a specific employee"""
    try:
        contacts = EmployeeEmergencyContactService.fetch_active_contacts_by_employee(db, employee_id)
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active emergency contacts for employee: {str(e)}"
        )


@router.get("/fetchPrimaryEmergencyContact/{employee_id}", response_model=Optional[EmployeeEmergencyContactResponse])
async def fetch_primary_emergency_contact(employee_id: int, db: Session = Depends(get_db)):
    """Get primary emergency contact for an employee"""
    try:
        contact = EmployeeEmergencyContactService.fetch_primary_emergency_contact(db, employee_id)
        return contact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching primary emergency contact: {str(e)}"
        )


@router.get("/fetchAllEmployeeEmergencyContacts", response_model=List[EmployeeEmergencyContactResponse])
async def fetch_all_employee_emergency_contacts(db: Session = Depends(get_db)):
    """Get all employee emergency contacts"""
    try:
        contacts = EmployeeEmergencyContactService.fetch_all_employee_emergency_contacts(db)
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee emergency contacts: {str(e)}"
        )


@router.get("/getEmployeeEmergencyContacts", response_model=EmployeeEmergencyContactListResponse)
async def get_employee_emergency_contacts(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    relation: Optional[str] = Query(None, description="Filter by relation"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("EmployeeEmergencyContactId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee emergency contacts with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEmergencyContactService.get_employee_emergency_contacts_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            relation=relation,
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
            detail=f"Error fetching employee emergency contacts: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeEmergencyContact")
async def insert_or_update_employee_emergency_contact(contact: dict, db: Session = Depends(get_db)):
    """Insert or update employee emergency contact"""
    try:
        response = EmployeeEmergencyContactService.insert_or_update_employee_emergency_contact(db, contact)
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
            detail=f"Error saving employee emergency contact: {str(e)}"
        )


@router.delete("/DeleteEmployeeEmergencyContact/{employee_emergency_contact_id}", response_model=EmployeeEmergencyContactDeleteResponse)
async def delete_employee_emergency_contact(employee_emergency_contact_id: int, db: Session = Depends(get_db)):
    """Delete employee emergency contact"""
    try:
        response = EmployeeEmergencyContactService.delete_employee_emergency_contact(db, employee_emergency_contact_id)
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
            detail=f"Error deleting employee emergency contact: {str(e)}"
        )


@router.patch("/SoftDeleteEmployeeEmergencyContact/{employee_emergency_contact_id}", response_model=EmployeeEmergencyContactResponse)
async def soft_delete_employee_emergency_contact(
    employee_emergency_contact_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee emergency contact (deactivate)"""
    try:
        response = EmployeeEmergencyContactService.soft_delete_employee_emergency_contact(
            db, employee_emergency_contact_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["contact"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee emergency contact: {str(e)}"
        )


@router.get("/checkEmployeeEmergencyContactExists", response_model=EmployeeEmergencyContactExistsResponse)
async def check_employee_emergency_contact_exists(
    employee_id: int = Query(..., description="Employee ID"),
    name: str = Query(..., description="Contact name"),
    relation: str = Query(..., description="Relationship"),
    db: Session = Depends(get_db)
):
    """Check if emergency contact exists for employee"""
    try:
        result = EmployeeEmergencyContactService.check_emergency_contact_exists(db, employee_id, name, relation)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee emergency contact existence: {str(e)}"
        )


@router.get("/getEmployeeEmergencyContactsSummary/{employee_id}", response_model=dict)
async def get_employee_emergency_contacts_summary(employee_id: int, db: Session = Depends(get_db)):
    """Get emergency contacts summary for an employee"""
    try:
        summary = EmployeeEmergencyContactService.get_employee_emergency_contacts_summary(db, employee_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching emergency contacts summary: {str(e)}"
        )


@router.post("/createBulkEmergencyContacts", response_model=List[EmployeeEmergencyContactResponse])
async def create_bulk_emergency_contacts(
    bulk_data: EmployeeEmergencyContactBulkCreate,
    db: Session = Depends(get_db)
):
    """Create multiple emergency contacts at once"""
    try:
        contacts = EmployeeEmergencyContactService.create_bulk_emergency_contacts(
            db, bulk_data.contacts, bulk_data.employee_id
        )
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bulk emergency contacts: {str(e)}"
        )


@router.patch("/setAsPrimaryContact/{employee_emergency_contact_id}", response_model=EmployeeEmergencyContactResponse)
async def set_as_primary_contact(
    employee_emergency_contact_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Set an emergency contact as primary"""
    try:
        response = EmployeeEmergencyContactService.update_contact_as_primary(
            db, employee_emergency_contact_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response["contact"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting contact as primary: {str(e)}"
        )


# Alternative endpoints using Pydantic models
@router.post("/create", response_model=EmployeeEmergencyContactCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_emergency_contact(
    contact: EmployeeEmergencyContactCreate, 
    db: Session = Depends(get_db)
):
    """Create a new employee emergency contact using Pydantic model"""
    try:
        # Check if emergency contact already exists
        exists_result = EmployeeEmergencyContactService.check_emergency_contact_exists(
            db, contact.EmployeeId, contact.Name, contact.Relation
        )
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Emergency contact already exists for this employee (ID: {exists_result['employee_emergency_contact_id']})"
            )
        
        db_contact = EmployeeEmergencyContactService.create_employee_emergency_contact(db, contact)
        return {
            "success": True,
            "message": "Employee emergency contact created successfully",
            "employee_emergency_contact_id": db_contact.EmployeeEmergencyContactId
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
            detail=f"Error creating employee emergency contact: {str(e)}"
        )


@router.put("/update/{employee_emergency_contact_id}", response_model=EmployeeEmergencyContactUpdateResponse)
async def update_employee_emergency_contact(
    employee_emergency_contact_id: int, 
    contact: EmployeeEmergencyContactUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing employee emergency contact using Pydantic model"""
    try:
        updated_contact = EmployeeEmergencyContactService.update_employee_emergency_contact(
            db, employee_emergency_contact_id, contact
        )
        if not updated_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee emergency contact with ID {employee_emergency_contact_id} not found"
            )
        
        # Get list of updated fields
        updated_fields = list(contact.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee emergency contact updated successfully",
            "employee_emergency_contact_id": employee_emergency_contact_id,
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
            detail=f"Error updating employee emergency contact: {str(e)}"
        )


@router.get("/emergencyContactStatistics", response_model=dict)
async def get_emergency_contact_statistics(db: Session = Depends(get_db)):
    """Get emergency contact statistics"""
    try:
        stats = EmployeeEmergencyContactService.get_emergency_contact_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching emergency contact statistics: {str(e)}"
        )


@router.get("/searchByRelation/{relation}", response_model=List[EmployeeEmergencyContactResponse])
async def search_by_relation(relation: str, db: Session = Depends(get_db)):
    """Search emergency contacts by relation"""
    try:
        items, _ = EmployeeEmergencyContactService.get_employee_emergency_contacts_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            relation=relation,
            is_active=True
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by relation: {str(e)}"
        )


@router.post("/searchEmployeeEmergencyContacts", response_model=EmployeeEmergencyContactListResponse)
async def search_employee_emergency_contacts(
    filters: EmployeeEmergencyContactFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeEmergencyContactId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee emergency contact search with filters"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEmergencyContactService.get_employee_emergency_contacts_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term,
            employee_id=filters.employee_id,
            relation=filters.relation,
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
            detail=f"Error searching employee emergency contacts: {str(e)}"
        )


@router.get("/employeesWithoutEmergencyContacts", response_model=List[int])
async def get_employees_without_emergency_contacts(db: Session = Depends(get_db)):
    """Get list of employee IDs without emergency contacts"""
    try:
        from app.models.employee import Employee
        from sqlalchemy import not_, exists
        
        # Get employees who don't have any active emergency contacts
        subquery = db.query(EmployeeEmergencyContact.EmployeeId).filter(
            EmployeeEmergencyContact.IsActive == True
        )
        
        employees_without_contacts = db.query(Employee.EmployeeId).filter(
            not_(Employee.EmployeeId.in_(subquery))
        ).all()
        
        return [emp.EmployeeId for emp in employees_without_contacts]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees without emergency contacts: {str(e)}"
        )