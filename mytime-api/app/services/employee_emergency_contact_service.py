from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.employee_emergency_contact import EmployeeEmergencyContact
from app.schemas.employee_emergency_contact_schemas import (
    EmployeeEmergencyContactCreate, 
    EmployeeEmergencyContactUpdate
)

class EmployeeEmergencyContactService:
    """Service for EmployeeEmergencyContact operations"""
    
    @staticmethod
    def fetch_employee_emergency_contact(
        db: Session, 
        employee_emergency_contact_id: int
    ) -> Optional[EmployeeEmergencyContact]:
        """Get employee emergency contact by ID"""
        return db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
        ).first()
    
    @staticmethod
    def fetch_contacts_by_employee(db: Session, employee_id: int) -> List[EmployeeEmergencyContact]:
        """Get all emergency contacts for a specific employee"""
        return db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id
        ).order_by(
            EmployeeEmergencyContact.Relation
        ).all()
    
    @staticmethod
    def fetch_active_contacts_by_employee(db: Session, employee_id: int) -> List[EmployeeEmergencyContact]:
        """Get active emergency contacts for a specific employee"""
        return db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id,
            EmployeeEmergencyContact.IsActive == True
        ).order_by(
            EmployeeEmergencyContact.Relation
        ).all()
    
    @staticmethod
    def fetch_primary_emergency_contact(db: Session, employee_id: int) -> Optional[EmployeeEmergencyContact]:
        """Get primary emergency contact for an employee (first active contact)"""
        return db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id,
            EmployeeEmergencyContact.IsActive == True
        ).order_by(
            EmployeeEmergencyContact.EmployeeEmergencyContactId
        ).first()
    
    @staticmethod
    def fetch_all_employee_emergency_contacts(db: Session) -> List[EmployeeEmergencyContact]:
        """Get all employee emergency contacts"""
        return db.query(EmployeeEmergencyContact).all()
    
    @staticmethod
    def get_employee_emergency_contacts_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        relation: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "EmployeeEmergencyContactId",
        sort_order: str = "desc"
    ) -> Tuple[List[EmployeeEmergencyContact], int]:
        """Get paginated employee emergency contacts with filtering and sorting"""
        query = db.query(EmployeeEmergencyContact)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(EmployeeEmergencyContact.Name, '').ilike(search_term),
                    func.coalesce(EmployeeEmergencyContact.Relation, '').ilike(search_term),
                    func.coalesce(EmployeeEmergencyContact.Phone, '').ilike(search_term),
                    func.coalesce(EmployeeEmergencyContact.Email, '').ilike(search_term),
                    func.coalesce(EmployeeEmergencyContact.Address, '').ilike(search_term)
                )
            )
        
        # Apply employee filter
        if employee_id:
            query = query.filter(EmployeeEmergencyContact.EmployeeId == employee_id)
        
        # Apply relation filter
        if relation:
            query = query.filter(func.lower(EmployeeEmergencyContact.Relation) == func.lower(relation))
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(EmployeeEmergencyContact.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(EmployeeEmergencyContact, sort_by, EmployeeEmergencyContact.EmployeeEmergencyContactId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_employee_emergency_contact(db: Session, contact_data: dict) -> Dict[str, Any]:
        """Insert or update employee emergency contact"""
        employee_emergency_contact_id = contact_data.get('EmployeeEmergencyContactId')
        
        if employee_emergency_contact_id:
            # Update existing contact
            db_contact = db.query(EmployeeEmergencyContact).filter(
                EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
            ).first()
            
            if not db_contact:
                return {"success": False, "message": "Employee emergency contact not found", "contact": None}
            
            # Update only non-null values
            for key, value in contact_data.items():
                if key != 'EmployeeEmergencyContactId' and value is not None:
                    setattr(db_contact, key, value)
            
            # Set ModifiedOn timestamp
            db_contact.ModifiedOn = datetime.utcnow()
            
            db.commit()
            db.refresh(db_contact)
            return {
                "success": True, 
                "message": "Employee emergency contact updated successfully",
                "contact": db_contact
            }
        else:
            # Create new contact
            # Remove EmployeeEmergencyContactId if present in create mode
            contact_data.pop('EmployeeEmergencyContactId', None)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in contact_data:
                contact_data['CreatedOn'] = datetime.utcnow()
            
            db_contact = EmployeeEmergencyContact(**contact_data)
            db.add(db_contact)
            db.commit()
            db.refresh(db_contact)
            return {
                "success": True, 
                "message": "Employee emergency contact created successfully",
                "contact": db_contact
            }
    
    @staticmethod
    def delete_employee_emergency_contact(db: Session, employee_emergency_contact_id: int) -> Dict[str, Any]:
        """Delete employee emergency contact"""
        db_contact = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
        ).first()
        
        if not db_contact:
            return {"success": False, "message": "Employee emergency contact not found"}
        
        db.delete(db_contact)
        db.commit()
        return {"success": True, "message": "Employee emergency contact deleted successfully"}
    
    @staticmethod
    def soft_delete_employee_emergency_contact(
        db: Session, 
        employee_emergency_contact_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee emergency contact (set IsActive = False)"""
        db_contact = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
        ).first()
        
        if not db_contact:
            return {"success": False, "message": "Employee emergency contact not found"}
        
        db_contact.IsActive = False
        db_contact.ModifiedBy = modified_by
        db_contact.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_contact)
        return {
            "success": True, 
            "message": "Employee emergency contact deactivated successfully",
            "contact": db_contact
        }
    
    @staticmethod
    def create_employee_emergency_contact(
        db: Session, 
        contact: EmployeeEmergencyContactCreate
    ) -> EmployeeEmergencyContact:
        """Create new employee emergency contact using Pydantic schema"""
        contact_data = contact.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in contact_data:
            contact_data['CreatedOn'] = datetime.utcnow()
        
        db_contact = EmployeeEmergencyContact(**contact_data)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    
    @staticmethod
    def update_employee_emergency_contact(
        db: Session, 
        employee_emergency_contact_id: int, 
        contact: EmployeeEmergencyContactUpdate
    ) -> Optional[EmployeeEmergencyContact]:
        """Update existing employee emergency contact using Pydantic schema"""
        db_contact = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
        ).first()
        
        if db_contact:
            update_data = contact.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                setattr(db_contact, key, value)
            
            db.commit()
            db.refresh(db_contact)
        
        return db_contact
    
    @staticmethod
    def check_emergency_contact_exists(
        db: Session, 
        employee_id: int, 
        name: str,
        relation: str
    ) -> Dict[str, Any]:
        """Check if emergency contact exists for employee"""
        contact = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id,
            func.lower(EmployeeEmergencyContact.Name) == func.lower(name),
            func.lower(EmployeeEmergencyContact.Relation) == func.lower(relation)
        ).first()
        
        return {
            "exists": contact is not None,
            "employee_emergency_contact_id": contact.EmployeeEmergencyContactId if contact else None
        }
    
    @staticmethod
    def get_employee_emergency_contacts_summary(db: Session, employee_id: int) -> Dict[str, Any]:
        """Get emergency contacts summary for an employee"""
        contacts = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id,
            EmployeeEmergencyContact.IsActive == True
        ).order_by(
            EmployeeEmergencyContact.Relation
        ).all()
        
        primary_contact = contacts[0] if contacts else None
        
        # Group by relation
        by_relation = {}
        for contact in contacts:
            relation = contact.Relation
            if relation not in by_relation:
                by_relation[relation] = []
            by_relation[relation].append({
                "id": contact.EmployeeEmergencyContactId,
                "name": contact.Name,
                "phone": contact.Phone,
                "email": contact.Email
            })
        
        return {
            "total_contacts": len(contacts),
            "primary_contact": primary_contact,
            "contacts_by_relation": by_relation,
            "all_contacts": contacts
        }
    
    @staticmethod
    def create_bulk_emergency_contacts(
        db: Session, 
        contacts: List[EmployeeEmergencyContactCreate],
        employee_id: Optional[int] = None
    ) -> List[EmployeeEmergencyContact]:
        """Create multiple emergency contacts at once"""
        db_contacts = []
        
        for contact_data in contacts:
            # If employee_id is provided, override the EmployeeId in each contact
            if employee_id:
                contact_data.EmployeeId = employee_id
            
            contact_dict = contact_data.model_dump(exclude_none=True)
            contact_dict['CreatedOn'] = datetime.utcnow()
            
            db_contact = EmployeeEmergencyContact(**contact_dict)
            db.add(db_contact)
            db_contacts.append(db_contact)
        
        db.commit()
        
        # Refresh all contacts
        for contact in db_contacts:
            db.refresh(contact)
        
        return db_contacts
    
    @staticmethod
    def get_emergency_contact_statistics(db: Session) -> Dict[str, Any]:
        """Get emergency contact statistics"""
        # Total records
        total_records = db.query(func.count(EmployeeEmergencyContact.EmployeeEmergencyContactId)).scalar()
        
        # Count by relation
        relation_counts = db.query(
            EmployeeEmergencyContact.Relation,
            func.count(EmployeeEmergencyContact.EmployeeEmergencyContactId).label('count')
        ).filter(
            EmployeeEmergencyContact.Relation.isnot(None),
            EmployeeEmergencyContact.IsActive == True
        ).group_by(
            EmployeeEmergencyContact.Relation
        ).all()
        
        # Employees with emergency contacts
        employees_with_contacts = db.query(
            func.count(func.distinct(EmployeeEmergencyContact.EmployeeId))
        ).filter(
            EmployeeEmergencyContact.IsActive == True
        ).scalar()
        
        return {
            "total_records": total_records,
            "by_relation": {relation: count for relation, count in relation_counts},
            "employees_with_contacts": employees_with_contacts,
            "common_relations": sorted(
                [(relation, count) for relation, count in relation_counts],
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 relations
        }
    
    @staticmethod
    def update_contact_as_primary(
        db: Session, 
        employee_emergency_contact_id: int,
        modified_by: int
    ) -> Dict[str, Any]:
        """Set an emergency contact as primary (deactivate others, activate this one)"""
        # Get the contact to update
        db_contact = db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeEmergencyContactId == employee_emergency_contact_id
        ).first()
        
        if not db_contact:
            return {"success": False, "message": "Emergency contact not found"}
        
        employee_id = db_contact.EmployeeId
        
        # First, deactivate all contacts for this employee
        db.query(EmployeeEmergencyContact).filter(
            EmployeeEmergencyContact.EmployeeId == employee_id
        ).update(
            {"IsActive": False, "ModifiedBy": modified_by, "ModifiedOn": datetime.utcnow()},
            synchronize_session=False
        )
        
        # Then activate the selected contact
        db_contact.IsActive = True
        db_contact.ModifiedBy = modified_by
        db_contact.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_contact)
        return {
            "success": True, 
            "message": "Emergency contact set as primary successfully",
            "contact": db_contact
        }