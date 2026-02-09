from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
import logging

from app.models.employee_address import EmployeeAddress
from app.schemas.employee_address_schemas import EmployeeAddressCreate, EmployeeAddressUpdate

logger = logging.getLogger(__name__)


class EmployeeAddressService:
    """Service for EmployeeAddress operations"""
    
    @staticmethod
    def fetch_employee_address(db: Session, employee_address_id: int) -> Optional[EmployeeAddress]:
        """Get employee address by ID"""
        try:
            return db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeAddressId == employee_address_id
            ).first()
        except Exception as e:
            logger.error(f"Error fetching employee address {employee_address_id}: {str(e)}")
            return None
    
    @staticmethod
    def fetch_addresses_by_employee(db: Session, employee_id: int) -> List[EmployeeAddress]:
        """Get all addresses for a specific employee"""
        try:
            return db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeId == employee_id
            ).order_by(
                asc(EmployeeAddress.IsActive.desc()),  # Active addresses first
                desc(EmployeeAddress.CreatedOn)  # Newest first
            ).all()
        except Exception as e:
            logger.error(f"Error fetching addresses for employee {employee_id}: {str(e)}")
            return []
    
    @staticmethod
    def fetch_active_addresses_by_employee(db: Session, employee_id: int) -> List[EmployeeAddress]:
        """Get active addresses for a specific employee"""
        try:
            return db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeId == employee_id,
                EmployeeAddress.IsActive == True
            ).order_by(
                desc(EmployeeAddress.CreatedOn)
            ).all()
        except Exception as e:
            logger.error(f"Error fetching active addresses for employee {employee_id}: {str(e)}")
            return []
    
    @staticmethod
    def fetch_all_employee_addresses(db: Session) -> List[EmployeeAddress]:
        """Get all employee addresses"""
        try:
            return db.query(EmployeeAddress).all()
        except Exception as e:
            logger.error(f"Error fetching all employee addresses: {str(e)}")
            return []
    
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
        try:
            query = db.query(EmployeeAddress)
            
            # Apply search filter
            if search and search.strip():
                search_term = f"%{search.strip()}%"
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
            sort_column_map = {
                "employee_address_id": EmployeeAddress.EmployeeAddressId,
                "employee_id": EmployeeAddress.EmployeeId,
                "city_id": EmployeeAddress.CityId,
                "state_id": EmployeeAddress.StateId,
                "country_id": EmployeeAddress.CountryId,
                "created_on": EmployeeAddress.CreatedOn,
                "is_active": EmployeeAddress.IsActive
            }
            
            sort_column = sort_column_map.get(
                sort_by.lower().replace(" ", "_"),
                EmployeeAddress.EmployeeAddressId
            )
            
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))
            
            # Apply pagination
            items = query.offset(skip).limit(limit).all()
            
            return items, total
            
        except Exception as e:
            logger.error(f"Error in get_employee_addresses_with_pagination: {str(e)}")
            return [], 0
    
    @staticmethod
    def insert_or_update_employee_address(db: Session, address_data: dict) -> Dict[str, Any]:
        """Insert or update employee address"""
        try:
            # Convert IDs to BigInteger if needed
            for id_field in ['EmployeeId', 'CityId', 'StateId', 'CountryId', 'CreatedBy', 'ModifiedBy']:
                if id_field in address_data and address_data[id_field] is not None:
                    try:
                        address_data[id_field] = int(address_data[id_field])
                    except (ValueError, TypeError):
                        address_data[id_field] = None
            
            employee_address_id = address_data.get('EmployeeAddressId')
            
            # Handle EmployeeAddressId properly
            if employee_address_id:
                try:
                    employee_address_id = int(employee_address_id)
                except (ValueError, TypeError):
                    employee_address_id = 0
            
            if employee_address_id and employee_address_id > 0:
                # Update existing address
                db_address = db.query(EmployeeAddress).filter(
                    EmployeeAddress.EmployeeAddressId == employee_address_id
                ).first()
                
                if not db_address:
                    return {
                        "success": False, 
                        "message": "Employee address not found", 
                        "address": None
                    }
                
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
                if 'CreatedOn' not in address_data or not address_data['CreatedOn']:
                    address_data['CreatedOn'] = datetime.utcnow()
                
                # Set default Active status if not provided
                if 'IsActive' not in address_data:
                    address_data['IsActive'] = True
                
                # Validate required fields
                if 'EmployeeId' not in address_data or not address_data['EmployeeId']:
                    return {
                        "success": False,
                        "message": "EmployeeId is required",
                        "address": None
                    }
                
                if 'AddressLineOne' not in address_data or not address_data['AddressLineOne']:
                    return {
                        "success": False,
                        "message": "AddressLineOne is required",
                        "address": None
                    }
                
                db_address = EmployeeAddress(**address_data)
                db.add(db_address)
                db.commit()
                db.refresh(db_address)
                
                return {
                    "success": True, 
                    "message": "Employee address created successfully",
                    "address": db_address
                }
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error in insert_or_update_employee_address: {str(e)}")
            return {
                "success": False, 
                "message": f"Error saving employee address: {str(e)}",
                "address": None
            }
    
    @staticmethod
    def delete_employee_address(db: Session, employee_address_id: int) -> Dict[str, Any]:
        """Delete employee address"""
        try:
            db_address = db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeAddressId == employee_address_id
            ).first()
            
            if not db_address:
                return {
                    "success": False, 
                    "message": "Employee address not found"
                }
            
            db.delete(db_address)
            db.commit()
            
            return {
                "success": True, 
                "message": "Employee address deleted successfully"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting employee address {employee_address_id}: {str(e)}")
            return {
                "success": False, 
                "message": f"Error deleting employee address: {str(e)}"
            }
    
    @staticmethod
    def soft_delete_employee_address(
        db: Session, 
        employee_address_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee address (set IsActive = False)"""
        try:
            db_address = db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeAddressId == employee_address_id
            ).first()
            
            if not db_address:
                return {
                    "success": False, 
                    "message": "Employee address not found"
                }
            
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
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error soft deleting employee address {employee_address_id}: {str(e)}")
            return {
                "success": False, 
                "message": f"Error deactivating employee address: {str(e)}"
            }
    
    @staticmethod
    def create_employee_address(db: Session, address: EmployeeAddressCreate) -> Optional[EmployeeAddress]:
        """Create new employee address using Pydantic schema"""
        try:
            address_data = address.model_dump(exclude_none=True)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in address_data:
                address_data['CreatedOn'] = datetime.utcnow()
            
            db_address = EmployeeAddress(**address_data)
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            
            return db_address
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating employee address: {str(e)}")
            return None
    
    @staticmethod
    def update_employee_address(
        db: Session, 
        employee_address_id: int, 
        address: EmployeeAddressUpdate
    ) -> Optional[EmployeeAddress]:
        """Update existing employee address using Pydantic schema"""
        try:
            db_address = db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeAddressId == employee_address_id
            ).first()
            
            if not db_address:
                return None
            
            update_data = address.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                if value is not None:
                    setattr(db_address, key, value)
            
            db.commit()
            db.refresh(db_address)
            
            return db_address
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating employee address {employee_address_id}: {str(e)}")
            return None
    
    @staticmethod
    def check_address_exists(
        db: Session, 
        employee_id: int, 
        address_line_one: str
    ) -> Dict[str, Any]:
        """Check if address exists for employee"""
        try:
            address = db.query(EmployeeAddress).filter(
                EmployeeAddress.EmployeeId == employee_id,
                func.lower(EmployeeAddress.AddressLineOne) == func.lower(address_line_one.strip())
            ).first()
            
            return {
                "exists": address is not None,
                "employee_address_id": address.EmployeeAddressId if address else None
            }
        except Exception as e:
            logger.error(f"Error checking address exists: {str(e)}")
            return {"exists": False, "employee_address_id": None}
    
    @staticmethod
    def set_primary_address(
        db: Session, 
        employee_id: int, 
        employee_address_id: int,
        modified_by: int
    ) -> Dict[str, Any]:
        """Set an address as primary (deactivate others)"""
        try:
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
                return {
                    "success": False, 
                    "message": "Employee address not found"
                }
            
            db_address.IsActive = True
            db_address.ModifiedBy = modified_by
            db_address.ModifiedOn = datetime.utcnow()
            
            db.commit()
            return {
                "success": True, 
                "message": "Primary address set successfully",
                "address": db_address
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error setting primary address: {str(e)}")
            return {
                "success": False, 
                "message": f"Error setting primary address: {str(e)}"
            }
    
    @staticmethod
    def create_bulk_addresses(
        db: Session, 
        addresses: List[EmployeeAddressCreate],
        employee_id: Optional[int] = None
    ) -> List[EmployeeAddress]:
        """Create multiple addresses at once"""
        try:
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
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating bulk addresses: {str(e)}")
            return []