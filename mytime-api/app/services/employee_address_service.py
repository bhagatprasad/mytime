from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.employee_address import EmployeeAddress
from app.schemas.employee_address_schemas import EmployeeAddressCreate, EmployeeAddressUpdate

class EmployeeAddressService:
    """Service for EmployeeAddress operations"""
    
    @staticmethod
    def fetch_employee_address(db: Session, employee_address_id: int) -> Optional[EmployeeAddress]:
        """Get employee address by ID"""
        return db.query(EmployeeAddress).filter(EmployeeAddress.EmployeeAddressId == employee_address_id).first()
    
    @staticmethod
    def fetch_addresses_by_employee(db: Session, employee_id: int) -> List[EmployeeAddress]:
        """Get all addresses for a specific employee"""
        return db.query(EmployeeAddress).filter(EmployeeAddress.EmployeeId == employee_id).all()
    
    @staticmethod
    def fetch_active_addresses_by_employee(db: Session, employee_id: int) -> List[EmployeeAddress]:
        """Get active addresses for a specific employee"""
        return db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeId == employee_id,
            EmployeeAddress.IsActive == True
        ).all()
    
    @staticmethod
    def fetch_all_employee_addresses(db: Session) -> List[EmployeeAddress]:
        """Get all employee addresses"""
        return db.query(EmployeeAddress).all()
    
    @staticmethod
    def get_employee_addresses_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        city_id: Optional[int] = None,
        state_id: Optional[int] = None,
        country_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "EmployeeAddressId",
        sort_order: str = "desc"
    ) -> Tuple[List[EmployeeAddress], int]:
        """Get paginated employee addresses with filtering and sorting"""
        query = db.query(EmployeeAddress)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(EmployeeAddress.HNo, '').ilike(search_term),
                    func.coalesce(EmployeeAddress.AddressLineOne, '').ilike(search_term),
                    func.coalesce(EmployeeAddress.AddressLineTwo, '').ilike(search_term),
                    func.coalesce(EmployeeAddress.Landmark, '').ilike(search_term),
                    func.coalesce(EmployeeAddress.Zipcode, '').ilike(search_term)
                )
            )
        
        # Apply employee filter
        if employee_id:
            query = query.filter(EmployeeAddress.EmployeeId == employee_id)
        
        # Apply city filter
        if city_id:
            query = query.filter(EmployeeAddress.CityId == city_id)
        
        # Apply state filter
        if state_id:
            query = query.filter(EmployeeAddress.StateId == state_id)
        
        # Apply country filter
        if country_id:
            query = query.filter(EmployeeAddress.CountryId == country_id)
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(EmployeeAddress.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(EmployeeAddress, sort_by, EmployeeAddress.EmployeeAddressId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_employee_address(db: Session, address_data: dict) -> Dict[str, Any]:
        """Insert or update employee address"""
        employee_address_id = address_data.get('EmployeeAddressId')
        
        if employee_address_id:
            # Update existing address
            db_address = db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeAddressId == employee_address_id
            ).first()
            
            if not db_address:
                return {"success": False, "message": "Employee address not found", "address": None}
            
            # Update only non-null values
            for key, value in address_data.items():
                if key != 'EmployeeAddressId' and value is not None:
                    setattr(db_address, key, value)
            
            # Set ModifiedOn timestamp
            db_address.ModifiedOn = datetime.utcnow()
            
            db.commit()
            db.refresh(db_address)
            return {
                "success": True, 
                "message": "Employee address updated successfully",
                "address": db_address
            }
        else:
            # Create new address
            # Remove EmployeeAddressId if present in create mode
            address_data.pop('EmployeeAddressId', None)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in address_data:
                address_data['CreatedOn'] = datetime.utcnow()
            
            db_address = EmployeeAddress(**address_data)
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            return {
                "success": True, 
                "message": "Employee address created successfully",
                "address": db_address
            }
    
    @staticmethod
    def delete_employee_address(db: Session, employee_address_id: int) -> Dict[str, Any]:
        """Delete employee address"""
        db_address = db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeAddressId == employee_address_id
        ).first()
        
        if not db_address:
            return {"success": False, "message": "Employee address not found"}
        
        db.delete(db_address)
        db.commit()
        return {"success": True, "message": "Employee address deleted successfully"}
    
    @staticmethod
    def soft_delete_employee_address(
        db: Session, 
        employee_address_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee address (set IsActive = False)"""
        db_address = db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeAddressId == employee_address_id
        ).first()
        
        if not db_address:
            return {"success": False, "message": "Employee address not found"}
        
        db_address.IsActive = False
        db_address.ModifiedBy = modified_by
        db_address.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_address)
        return {
            "success": True, 
            "message": "Employee address deactivated successfully",
            "address": db_address
        }
    
    @staticmethod
    def create_employee_address(db: Session, address: EmployeeAddressCreate) -> EmployeeAddress:
        """Create new employee address using Pydantic schema"""
        address_data = address.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in address_data:
            address_data['CreatedOn'] = datetime.utcnow()
        
        db_address = EmployeeAddress(**address_data)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    
    @staticmethod
    def update_employee_address(
        db: Session, 
        employee_address_id: int, 
        address: EmployeeAddressUpdate
    ) -> Optional[EmployeeAddress]:
        """Update existing employee address using Pydantic schema"""
        db_address = db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeAddressId == employee_address_id
        ).first()
        
        if db_address:
            update_data = address.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                setattr(db_address, key, value)
            
            db.commit()
            db.refresh(db_address)
        
        return db_address
    
    @staticmethod
    def check_address_exists(
        db: Session, 
        employee_id: int, 
        address_line_one: str
    ) -> Dict[str, Any]:
        """Check if address exists for employee"""
        address = db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeId == employee_id,
            func.lower(EmployeeAddress.AddressLineOne) == func.lower(address_line_one)
        ).first()
        
        return {
            "exists": address is not None,
            "employee_address_id": address.EmployeeAddressId if address else None
        }
    
    @staticmethod
    def set_primary_address(
        db: Session, 
        employee_id: int, 
        employee_address_id: int,
        modified_by: int
    ) -> Dict[str, Any]:
        """Set an address as primary (deactivate others)"""
        # First, deactivate all addresses for this employee
        db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeId == employee_id
        ).update(
            {"IsActive": False, "ModifiedBy": modified_by, "ModifiedOn": datetime.utcnow()},
            synchronize_session=False
        )
        
        # Then activate the selected address
        db_address = db.query(EmployeeAddress).filter(
            EmployeeAddress.EmployeeAddressId == employee_address_id,
            EmployeeAddress.EmployeeId == employee_id
        ).first()
        
        if not db_address:
            db.rollback()
            return {"success": False, "message": "Employee address not found"}
        
        db_address.IsActive = True
        db_address.ModifiedBy = modified_by
        db_address.ModifiedOn = datetime.utcnow()
        
        db.commit()
        return {
            "success": True, 
            "message": "Primary address set successfully",
            "address": db_address
        }
    
    @staticmethod
    def create_bulk_addresses(
        db: Session, 
        addresses: List[EmployeeAddressCreate],
        employee_id: Optional[int] = None
    ) -> List[EmployeeAddress]:
        """Create multiple addresses at once"""
        db_addresses = []
        
        for address_data in addresses:
            # If employee_id is provided, override the EmployeeId in each address
            if employee_id:
                address_data.EmployeeId = employee_id
            
            address_dict = address_data.model_dump(exclude_none=True)
            address_dict['CreatedOn'] = datetime.utcnow()
            
            db_address = EmployeeAddress(**address_dict)
            db.add(db_address)
            db_addresses.append(db_address)
        
        db.commit()
        
        # Refresh all addresses
        for address in db_addresses:
            db.refresh(address)
        
        return db_addresses