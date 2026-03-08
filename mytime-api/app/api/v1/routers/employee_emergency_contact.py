from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.employee_emergency_contact import EmployeeEmergencyContact
from app.schemas.employee_emergency_contact_schemas import (
     EmployeeEmergencyContactResponse,
     EmployeeEmergencyContactDeleteResponse
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