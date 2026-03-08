from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.document_type import DocumentType
from app.schemas.document_type_schemas import DocumentTypeCreate, DocumentTypeUpdate


class DocumentTypeService:
    """Service for DocumentType operations"""
    
    @staticmethod
    def fetch_document_type(db: Session, document_type_id: int) -> Optional[DocumentType]:
        """Get document type by ID"""
        return db.query(DocumentType).filter(DocumentType.Id == document_type_id).first()
    
    @staticmethod
    def fetch_all_document_types(db: Session) -> List[DocumentType]:
        """Get all document types"""
        return db.query(DocumentType).order_by(DocumentType.Name).all()
    
    @staticmethod
    def fetch_active_document_types(db: Session) -> List[DocumentType]:
        """Get all active document types"""
        return db.query(DocumentType).filter(
            DocumentType.IsActive == True
        ).order_by(DocumentType.Name).all()
    
    @staticmethod
    def get_document_types_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[DocumentType], int]:
        """Get paginated document types with filtering and sorting"""
        query = db.query(DocumentType)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                func.coalesce(DocumentType.Name, '').ilike(search_term)
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(DocumentType.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(DocumentType, sort_by, DocumentType.Id)
        except AttributeError:
            sort_column = DocumentType.Id
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_document_type_exists(db: Session, name: Optional[str] = None, 
                                  exclude_id: Optional[int] = None) -> bool:
        """Check if a document type with the same name exists"""
        if not name:
            return False
        
        query = db.query(DocumentType).filter(
            func.lower(DocumentType.Name) == func.lower(name)
        )
        
        if exclude_id:
            query = query.filter(DocumentType.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def insert_or_update_document_type(db: Session, document_type_data: dict) -> Dict[str, Any]:
        """Insert or update document type"""
        document_type_id = document_type_data.get('Id')
        
        if document_type_id:
            # Update existing document type
            db_document_type = db.query(DocumentType).filter(DocumentType.Id == document_type_id).first()
            if not db_document_type:
                return {"success": False, "message": "Document type not found", "document_type": None}
            
            # Check for duplicate name
            name = document_type_data.get('Name')
            
            if name and name != db_document_type.Name:
                if DocumentTypeService.check_document_type_exists(db, name, document_type_id):
                    return {
                        "success": False, 
                        "message": "Document type with same name already exists",
                        "document_type": None
                    }
            
            for key, value in document_type_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_document_type, key, value)
            
            db.commit()
            db.refresh(db_document_type)
            return {
                "success": True, 
                "message": "Document type updated successfully",
                "document_type": db_document_type
            }
        else:
            # Create new document type
            # Check for duplicate name
            name = document_type_data.get('Name')
            
            if DocumentTypeService.check_document_type_exists(db, name):
                return {
                    "success": False, 
                    "message": "Document type with same name already exists",
                    "document_type": None
                }
            
            # Remove Id if present in create mode
            document_type_data.pop('Id', None)
            db_document_type = DocumentType(**document_type_data)
            db.add(db_document_type)
            db.commit()
            db.refresh(db_document_type)
            return {
                "success": True, 
                "message": "Document type created successfully",
                "document_type": db_document_type
            }
    
    @staticmethod
    def delete_document_type(db: Session, document_type_id: int) -> Dict[str, Any]:
        """Delete document type"""
        db_document_type = db.query(DocumentType).filter(DocumentType.Id == document_type_id).first()
        if not db_document_type:
            return {"success": False, "message": "Document type not found"}
        
        db.delete(db_document_type)
        db.commit()
        return {"success": True, "message": "Document type deleted successfully"}
    
    @staticmethod
    def create_document_type(db: Session, document_type: DocumentTypeCreate) -> DocumentType:
        """Create new document type"""
        # Check for duplicate name
        if DocumentTypeService.check_document_type_exists(db, document_type.Name):
            raise ValueError("Document type with same name already exists")
        
        db_document_type = DocumentType(**document_type.model_dump(exclude_none=True))
        db.add(db_document_type)
        db.commit()
        db.refresh(db_document_type)
        return db_document_type
    
    @staticmethod
    def update_document_type(db: Session, document_type_id: int, document_type: DocumentTypeUpdate) -> Optional[DocumentType]:
        """Update existing document type"""
        db_document_type = db.query(DocumentType).filter(DocumentType.Id == document_type_id).first()
        if db_document_type:
            # Check for duplicate name
            update_data = document_type.model_dump(exclude_none=True)
            name = update_data.get('Name')
            
            if name and name != db_document_type.Name:
                if DocumentTypeService.check_document_type_exists(db, name, document_type_id):
                    raise ValueError("Document type with same name already exists")
            
            for key, value in update_data.items():
                setattr(db_document_type, key, value)
            db.commit()
            db.refresh(db_document_type)
        return db_document_type
    
    @staticmethod
    def toggle_active_status(db: Session, document_type_id: int, is_active: bool) -> Optional[DocumentType]:
        """Toggle the active status of a document type"""
        db_document_type = db.query(DocumentType).filter(DocumentType.Id == document_type_id).first()
        if db_document_type:
            db_document_type.IsActive = is_active
            db.commit()
            db.refresh(db_document_type)
        return db_document_type
    
    @staticmethod
    def search_document_types(db: Session, search_term: str, limit: int = 10) -> List[DocumentType]:
        """Search document types by name"""
        search_pattern = f"%{search_term}%"
        return db.query(DocumentType).filter(
            func.coalesce(DocumentType.Name, '').ilike(search_pattern)
        ).order_by(DocumentType.Name).limit(limit).all()
    
    @staticmethod
    def get_document_types_by_ids(db: Session, document_type_ids: List[int]) -> List[DocumentType]:
        """Get multiple document types by their IDs"""
        return db.query(DocumentType).filter(DocumentType.Id.in_(document_type_ids)).all()