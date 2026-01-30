from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.document_type_schemas import (
    DocumentTypeCreate, DocumentTypeUpdate, DocumentTypeResponse, DocumentTypeListResponse,
    DocumentTypeExistsResponse, DocumentTypeDeleteResponse
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


@router.get("/fetchActiveDocumentTypes", response_model=List[DocumentTypeResponse])
async def fetch_active_document_types(db: Session = Depends(get_db)):
    """Get all active document types"""
    try:
        document_types = DocumentTypeService.fetch_active_document_types(db)
        return document_types
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active document types: {str(e)}"
        )


@router.get("/getDocumentTypes", response_model=DocumentTypeListResponse)
async def get_document_types(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("Id", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated document types with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = DocumentTypeService.get_document_types_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active,
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
            detail=f"Error fetching document types: {str(e)}"
        )


@router.get("/checkDocumentTypeExists", response_model=DocumentTypeExistsResponse)
async def check_document_type_exists(
    name: Optional[str] = Query(None, description="Document type name"),
    exclude_id: Optional[int] = Query(None, description="Document type ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if document type exists"""
    try:
        exists = DocumentTypeService.check_document_type_exists(db, name, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking document type existence: {str(e)}"
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


@router.post("/create", response_model=DocumentTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_document_type(document_type: DocumentTypeCreate, db: Session = Depends(get_db)):
    """Create a new document type using Pydantic model"""
    try:
        return DocumentTypeService.create_document_type(db, document_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating document type: {str(e)}"
        )


@router.put("/update/{document_type_id}", response_model=DocumentTypeResponse)
async def update_document_type(document_type_id: int, document_type: DocumentTypeUpdate, db: Session = Depends(get_db)):
    """Update an existing document type using Pydantic model"""
    try:
        updated_document_type = DocumentTypeService.update_document_type(db, document_type_id, document_type)
        if not updated_document_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document type with ID {document_type_id} not found"
            )
        return updated_document_type
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
            detail=f"Error updating document type: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{document_type_id}", response_model=DocumentTypeResponse)
async def toggle_active_status(
    document_type_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a document type"""
    try:
        document_type = DocumentTypeService.toggle_active_status(db, document_type_id, is_active)
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
            detail=f"Error toggling active status: {str(e)}"
        )


@router.get("/searchDocumentTypes", response_model=List[DocumentTypeResponse])
async def search_document_types(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search document types by name"""
    try:
        document_types = DocumentTypeService.search_document_types(db, q, limit)
        return document_types
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching document types: {str(e)}"
        )


@router.get("/getDocumentTypesByIds", response_model=List[DocumentTypeResponse])
async def get_document_types_by_ids(
    ids: str = Query(..., description="Comma-separated document type IDs"),
    db: Session = Depends(get_db)
):
    """Get multiple document types by their IDs"""
    try:
        # Convert comma-separated string to list of integers
        document_type_ids = [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]
        
        if not document_type_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid document type IDs provided"
            )
        
        document_types = DocumentTypeService.get_document_types_by_ids(db, document_type_ids)
        return document_types
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document type ID format. Provide comma-separated integers."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching document types by IDs: {str(e)}"
        )