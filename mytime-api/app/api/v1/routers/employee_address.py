from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.employee_address_schemas import (
   EmployeeAddressResponse,
    EmployeeAddressDeleteResponse
)
from app.core.database import get_db
from app.services.employee_address_service import EmployeeAddressService

router = APIRouter()


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