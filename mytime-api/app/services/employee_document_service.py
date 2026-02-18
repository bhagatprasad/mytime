from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.employee_document import EmployeeDocument


class EmployeeDocumentService:
    """Service for Employee Document operations"""

    @staticmethod
    def fetch_all_documents(
        db: Session
    ) -> List[EmployeeDocument]:
        """Get all documents"""
        return db.query(EmployeeDocument).order_by(desc(EmployeeDocument.UploadTimestamp)).all()

    @staticmethod
    def fetch_employee_document(
        db: Session,
        employee_document_id: int
    ) -> Optional[EmployeeDocument]:
        """Get employee document by ID"""
        return db.query(EmployeeDocument).filter(
            EmployeeDocument.EmployeeDocumentId == employee_document_id
        ).first()

    @staticmethod
    def fetch_documents_by_employee(
        db: Session,
        employee_id: int
    ) -> List[EmployeeDocument]:
        """Get all documents for a specific employee"""
        return db.query(EmployeeDocument).filter(
            EmployeeDocument.EmployeeId == employee_id
        ).order_by(desc(EmployeeDocument.UploadTimestamp)).all()
    
   

    @staticmethod
    def insert_or_update_employee_document(
        db: Session,
        document_data: dict
    ) -> Dict[str, Any]:
        """Insert or update employee document"""

        document_id = document_data.get("EmployeeDocumentId")

        if document_id:
            # Update
            db_document = db.query(EmployeeDocument).filter(
                EmployeeDocument.EmployeeDocumentId == document_id
            ).first()

            if not db_document:
                return {"success": False, "message": "Document not found", "document": None}

            for key, value in document_data.items():
                if key != "EmployeeDocumentId" and value is not None:
                    setattr(db_document, key, value)

            db.commit()
            db.refresh(db_document)

            return {
                "success": True,
                "message": "Document updated successfully",
                "document": db_document
            }

        else:
            # Create
            document_data.pop("EmployeeDocumentId", None)

            if not document_data.get("UploadTimestamp"):
                document_data["UploadTimestamp"] = datetime.utcnow()

            db_document = EmployeeDocument(**document_data)
            db.add(db_document)
            db.commit()
            db.refresh(db_document)

            return {
                "success": True,
                "message": "Document created successfully",
                "document": db_document
            }

    @staticmethod
    def delete_employee_document(
        db: Session,
        employee_document_id: int
    ) -> Dict[str, Any]:
        """Delete document"""

        db_document = db.query(EmployeeDocument).filter(
            EmployeeDocument.EmployeeDocumentId == employee_document_id
        ).first()

        if not db_document:
            return {"success": False, "message": "Document not found"}

        db.delete(db_document)
        db.commit()

        return {"success": True, "message": "Document deleted successfully"}