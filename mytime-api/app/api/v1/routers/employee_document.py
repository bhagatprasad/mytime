from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.employee_document_schemas import (
    EmployeeDocumentResponse,
    EmployeeDocumentDeleteResponse
)
from app.core.database import get_db
from app.services.employee_document_service import EmployeeDocumentService

router = APIRouter()


@router.get("/fetchEmployeeDocuments",response_model=List[EmployeeDocumentResponse])
async def fetch_employee_documents(db:Session=Depends(get_db)):
    """
    Docstring for fetch_employee_documents
    
    :param db: Description
    :type db: Session
    """
    try:
        documents=EmployeeDocumentService.fetch_all_documents(db)
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching documents for employee: {str(e)}"
        )
@router.get("/fetchEmployeeDocument/{employee_document_id}", response_model=EmployeeDocumentResponse)
async def fetch_employee_document(
    employee_document_id: int,
    db: Session = Depends(get_db)
):
    """Get employee document by ID"""
    try:
        document = EmployeeDocumentService.fetch_employee_document(
            db, employee_document_id
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee document with ID {employee_document_id} not found"
            )

        return document

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee document: {str(e)}"
        )


@router.get("/fetchDocumentsByEmployee/{employee_id}", response_model=List[EmployeeDocumentResponse])
async def fetch_documents_by_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get all documents for a specific employee"""
    try:
        documents = EmployeeDocumentService.fetch_documents_by_employee(
            db, employee_id
        )
        return documents

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching documents for employee: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeDocument")
async def insert_or_update_employee_document(
    document: dict,
    db: Session = Depends(get_db)
):
    """Insert or update employee document"""
    try:
        response = EmployeeDocumentService.insert_or_update_employee_document(
            db, document
        )

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
            detail=f"Error saving employee document: {str(e)}"
        )


@router.delete("/DeleteEmployeeDocument/{employee_document_id}", response_model=EmployeeDocumentDeleteResponse)
async def delete_employee_document(
    employee_document_id: int,
    db: Session = Depends(get_db)
):
    """Delete employee document"""
    try:
        response = EmployeeDocumentService.delete_employee_document(
            db, employee_document_id
        )

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
            detail=f"Error deleting employee document: {str(e)}"
        )
