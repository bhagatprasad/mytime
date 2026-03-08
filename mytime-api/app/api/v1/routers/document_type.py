from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.document_type_schemas import (
    DocumentTypeResponse,
    DocumentTypeDeleteResponse
)
from app.core.database import get_db
from app.services.document_type_service import DocumentTypeService

router = APIRouter()


@router.get("/fetchDocumentType/{document_type_id}", response_model=DocumentTypeResponse)
async def fetch_document_type(document_type_id: int, db: Session = Depends(get_db)):
    """Get document type by ID"""
    try:
        document_type = DocumentTypeService.fetch_document_type(db, document_type_id)
        if not document_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document type with ID {document_type_id} not found"
            )
        return document_type
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching document type: {str(e)}"
        )


@router.get("/fetchAllDocumentTypes", response_model=List[DocumentTypeResponse])
async def fetch_all_document_types(db: Session = Depends(get_db)):
    """Get all document types"""
    try:
        document_types = DocumentTypeService.fetch_all_document_types(db)
        return document_types
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching document types: {str(e)}"
        )

@router.post("/InsertOrUpdateDocumentType")
async def insert_or_update_document_type(document_type: dict, db: Session = Depends(get_db)):
    """Insert or update document type"""
    try:
        response = DocumentTypeService.insert_or_update_document_type(db, document_type)
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
            detail=f"Error saving document type: {str(e)}"
        )


@router.delete("/DeleteDocumentType/{document_type_id}", response_model=DocumentTypeDeleteResponse)
async def delete_document_type(document_type_id: int, db: Session = Depends(get_db)):
    """Delete document type"""
    try:
        response = DocumentTypeService.delete_document_type(db, document_type_id)
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
            detail=f"Error deleting document type: {str(e)}"
        )