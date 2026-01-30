from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func, select
from sqlalchemy.orm import joinedload
from typing import Optional, List, Tuple, Dict, Any

from app.models.city import City
from app.models.country import Country
from app.models.state import State
from app.schemas.city_schemas import CityCreate, CityUpdate


class CityService:
    """Service for City operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_city(db: Session, city_id: int) -> Optional[City]:
        """Get city by ID - matches fetchCity in C#"""
        return db.query(City).filter(City.Id == city_id).first()
    
    @staticmethod
    def fetch_city_with_relations(db: Session, city_id: int) -> Optional[Dict[str, Any]]:
        """Get city by ID with country and state relations"""
        city = db.query(City).filter(City.Id == city_id).first()
        if not city:
            return None
        
        result = {
            "Id": city.Id,
            "Name": city.Name,
            "Code": city.Code,
            "CountryId": city.CountryId,
            "StateId": city.StateId,
            "CreatedBy": city.CreatedBy,
            "CreatedOn": city.CreatedOn,
            "ModifiedBy": city.ModifiedBy,
            "ModifiedOn": city.ModifiedOn,
            "IsActive": city.IsActive
        }
        
        # Get country info
        if city.CountryId:
            country = db.query(Country).filter(Country.Id == city.CountryId).first()
            if country:
                result["CountryName"] = country.Name
                result["CountryCode"] = country.Code
        
        # Get state info
        if city.StateId:
            state = db.query(State).filter(State.StateId == city.StateId).first()
            if state:
                result["StateName"] = state.Name
                result["StateCode"] = state.SateCode
        
        return result
    
    @staticmethod
    def fetch_all_cities(db: Session) -> List[City]:
        """Get all cities - matches fetchAllCities in C#"""
        return db.query(City).order_by(City.Name).all()
    
    @staticmethod
    def fetch_active_cities(db: Session) -> List[City]:
        """Get all active cities"""
        return db.query(City).filter(
            City.IsActive == True
        ).order_by(City.Name).all()
    
    @staticmethod
    def get_cities_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        country_id: Optional[int] = None,
        state_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[City], int]:
        """Get paginated cities with filtering and sorting"""
        query = db.query(City)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(City.Name, '').ilike(search_term),
                    func.coalesce(City.Code, '').ilike(search_term)
                )
            )
        
        # Apply country filter
        if country_id is not None:
            query = query.filter(City.CountryId == country_id)
        
        # Apply state filter
        if state_id is not None:
            query = query.filter(City.StateId == state_id)
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(City.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(City, sort_by, City.Id)
        except AttributeError:
            sort_column = City.Id
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def get_cities_with_relations_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        country_id: Optional[int] = None,
        state_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Get paginated cities with country and state relations"""
        # Build the base query
        query = db.query(
            City,
            Country.Name.label("CountryName"),
            Country.Code.label("CountryCode"),
            State.Name.label("StateName"),
            State.SateCode.label("StateCode")
        )
        
        # Join with Country and State tables
        query = query.outerjoin(Country, City.CountryId == Country.Id)
        query = query.outerjoin(State, City.StateId == State.StateId)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(City.Name, '').ilike(search_term),
                    func.coalesce(City.Code, '').ilike(search_term),
                    func.coalesce(Country.Name, '').ilike(search_term),
                    func.coalesce(State.Name, '').ilike(search_term)
                )
            )
        
        if country_id is not None:
            query = query.filter(City.CountryId == country_id)
        
        if state_id is not None:
            query = query.filter(City.StateId == state_id)
        
        if is_active is not None:
            query = query.filter(City.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting and pagination
        query = query.order_by(City.Name)
        results = query.offset(skip).limit(limit).all()
        
        # Format results
        items = []
        for city, country_name, country_code, state_name, state_code in results:
            items.append({
                "Id": city.Id,
                "Name": city.Name,
                "Code": city.Code,
                "CountryId": city.CountryId,
                "StateId": city.StateId,
                "CountryName": country_name,
                "CountryCode": country_code,
                "StateName": state_name,
                "StateCode": state_code,
                "CreatedBy": city.CreatedBy,
                "CreatedOn": city.CreatedOn,
                "ModifiedBy": city.ModifiedBy,
                "ModifiedOn": city.ModifiedOn,
                "IsActive": city.IsActive
            })
        
        return items, total
    
    @staticmethod
    def check_city_exists(db: Session, name: Optional[str] = None, 
                         code: Optional[str] = None, 
                         country_id: Optional[int] = None,
                         state_id: Optional[int] = None,
                         exclude_id: Optional[int] = None) -> bool:
        """Check if a city with the same name or code exists in same location"""
        query = db.query(City)
        
        conditions = []
        if name and country_id:
            conditions.append(
                (func.lower(City.Name) == func.lower(name)) & 
                (City.CountryId == country_id)
            )
        if code and country_id:
            conditions.append(
                (func.lower(City.Code) == func.lower(code)) & 
                (City.CountryId == country_id)
            )
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if state_id:
            query = query.filter(City.StateId == state_id)
        
        if exclude_id:
            query = query.filter(City.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_cities_by_country(db: Session, country_id: int) -> List[City]:
        """Get all cities for a specific country"""
        return db.query(City).filter(
            City.CountryId == country_id,
            City.IsActive == True
        ).order_by(City.Name).all()
    
    @staticmethod
    def get_cities_by_state(db: Session, state_id: int) -> List[City]:
        """Get all cities for a specific state"""
        return db.query(City).filter(
            City.StateId == state_id,
            City.IsActive == True
        ).order_by(City.Name).all()
    
    @staticmethod
    def get_city_by_code(db: Session, code: str, country_id: Optional[int] = None) -> Optional[City]:
        """Get city by code"""
        query = db.query(City).filter(func.lower(City.Code) == func.lower(code))
        
        if country_id:
            query = query.filter(City.CountryId == country_id)
        
        return query.first()
    
    @staticmethod
    def insert_or_update_city(db: Session, city_data: dict) -> Dict[str, Any]:
        """Insert or update city - matches InsertOrUpdateCity in C#"""
        city_id = city_data.get('Id')
        
        if city_id:
            # Update existing city
            db_city = db.query(City).filter(City.Id == city_id).first()
            if not db_city:
                return {"success": False, "message": "City not found", "city": None}
            
            # Check for duplicate name or code
            name = city_data.get('Name')
            code = city_data.get('Code')
            country_id = city_data.get('CountryId', db_city.CountryId)
            state_id = city_data.get('StateId', db_city.StateId)
            
            if (name and country_id) or (code and country_id):
                if CityService.check_city_exists(db, name, code, country_id, state_id, city_id):
                    return {
                        "success": False, 
                        "message": "City with same name or code already exists in this location",
                        "city": None
                    }
            
            for key, value in city_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_city, key, value)
            
            db.commit()
            db.refresh(db_city)
            return {
                "success": True, 
                "message": "City updated successfully",
                "city": db_city
            }
        else:
            # Create new city
            # Check for duplicate name or code
            name = city_data.get('Name')
            code = city_data.get('Code')
            country_id = city_data.get('CountryId')
            state_id = city_data.get('StateId')
            
            if CityService.check_city_exists(db, name, code, country_id, state_id):
                return {
                    "success": False, 
                    "message": "City with same name or code already exists in this location",
                    "city": None
                }
            
            # Remove Id if present in create mode
            city_data.pop('Id', None)
            db_city = City(**city_data)
            db.add(db_city)
            db.commit()
            db.refresh(db_city)
            return {
                "success": True, 
                "message": "City created successfully",
                "city": db_city
            }
    
    @staticmethod
    def delete_city(db: Session, city_id: int) -> Dict[str, Any]:
        """Delete city - matches DeleteCity in C#"""
        db_city = db.query(City).filter(City.Id == city_id).first()
        if not db_city:
            return {"success": False, "message": "City not found"}
        
        db.delete(db_city)
        db.commit()
        return {"success": True, "message": "City deleted successfully"}
    
    @staticmethod
    def create_city(db: Session, city: CityCreate) -> City:
        """Create new city"""
        # Check for duplicate name or code
        if CityService.check_city_exists(db, city.Name, city.Code, city.CountryId, city.StateId):
            raise ValueError("City with same name or code already exists in this location")
        
        db_city = City(**city.model_dump(exclude_none=True))
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    
    @staticmethod
    def update_city(db: Session, city_id: int, city: CityUpdate) -> Optional[City]:
        """Update existing city"""
        db_city = db.query(City).filter(City.Id == city_id).first()
        if db_city:
            # Check for duplicate name or code
            update_data = city.model_dump(exclude_none=True)
            name = update_data.get('Name')
            code = update_data.get('Code')
            country_id = update_data.get('CountryId', db_city.CountryId)
            state_id = update_data.get('StateId', db_city.StateId)
            
            if (name and country_id) or (code and country_id):
                if CityService.check_city_exists(db, name, code, country_id, state_id, city_id):
                    raise ValueError("City with same name or code already exists in this location")
            
            for key, value in update_data.items():
                setattr(db_city, key, value)
            db.commit()
            db.refresh(db_city)
        return db_city
    
    @staticmethod
    def toggle_active_status(db: Session, city_id: int, is_active: bool) -> Optional[City]:
        """Toggle the active status of a city"""
        db_city = db.query(City).filter(City.Id == city_id).first()
        if db_city:
            db_city.IsActive = is_active
            db.commit()
            db.refresh(db_city)
        return db_city
    
    @staticmethod
    def search_cities(db: Session, search_term: str, limit: int = 10) -> List[City]:
        """Search cities by name or code"""
        search_pattern = f"%{search_term}%"
        return db.query(City).filter(
            or_(
                func.coalesce(City.Name, '').ilike(search_pattern),
                func.coalesce(City.Code, '').ilike(search_pattern)
            )
        ).order_by(City.Name).limit(limit).all()
    
    @staticmethod
    def get_cities_by_ids(db: Session, city_ids: List[int]) -> List[City]:
        """Get multiple cities by their IDs"""
        return db.query(City).filter(City.Id.in_(city_ids)).all()
    
    @staticmethod
    def get_cities_by_country_and_state(db: Session, country_id: int, state_id: Optional[int] = None) -> List[City]:
        """Get cities by country and optionally state"""
        query = db.query(City).filter(
            City.CountryId == country_id,
            City.IsActive == True
        )
        
        if state_id:
            query = query.filter(City.StateId == state_id)
        
        return query.order_by(City.Name).all()