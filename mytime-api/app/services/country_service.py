from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.country import Country
from app.schemas.country_schemas import CountryCreate, CountryUpdate


class CountryService:
    @staticmethod
    def fetch_country(db: Session, country_id: int) -> Optional[Country]:
        return db.query(Country).filter(Country.Id == country_id).first()
    
    @staticmethod
    def fetch_all_countries(db: Session) -> List[Country]:
        return db.query(Country).order_by(Country.Name).all()
    
    @staticmethod
    def fetch_active_countries(db: Session) -> List[Country]:
        return db.query(Country).filter(
            Country.IsActive == True
        ).order_by(Country.Name).all()
    
    @staticmethod
    def get_countries_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[Country], int]:
        query = db.query(Country)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Country.Name, '').ilike(search_term),
                    func.coalesce(Country.Code, '').ilike(search_term)
                )
            )
        
        if is_active is not None:
            query = query.filter(Country.IsActive == is_active)
        
        total = query.count()
        
        try:
            sort_column = getattr(Country, sort_by, Country.Id)
        except AttributeError:
            sort_column = Country.Id
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_country_exists(db: Session, name: Optional[str] = None, 
                           code: Optional[str] = None, exclude_id: Optional[int] = None) -> bool:
        query = db.query(Country)
        
        conditions = []
        if name:
            conditions.append(func.lower(Country.Name) == func.lower(name))
        if code:
            conditions.append(func.lower(Country.Code) == func.lower(code))
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(Country.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_country_by_code(db: Session, code: str) -> Optional[Country]:
        return db.query(Country).filter(
            func.lower(Country.Code) == func.lower(code)
        ).first()
    
    @staticmethod
    def insert_or_update_country(db: Session, country_data: dict) -> Dict[str, Any]:
        country_id = country_data.get('Id')
        
        if country_id:
            # Update existing country
            db_country = db.query(Country).filter(Country.Id == country_id).first()
            if not db_country:
                return {"success": False, "message": "Country not found", "country": None}
            
            # Check for duplicate name or code
            name = country_data.get('Name')
            code = country_data.get('Code')
            
            if name or code:
                if CountryService.check_country_exists(db, name, code, country_id):
                    return {
                        "success": False, 
                        "message": "Country with same name or code already exists",
                        "country": None
                    }
            
            for key, value in country_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_country, key, value)
            
            db.commit()
            db.refresh(db_country)
            return {
                "success": True, 
                "message": "Country updated successfully",
                "country": db_country
            }
        else:
            name = country_data.get('Name')
            code = country_data.get('Code')
            
            if CountryService.check_country_exists(db, name, code):
                return {
                    "success": False, 
                    "message": "Country with same name or code already exists",
                    "country": None
                }
            
            country_data.pop('Id', None)
            db_country = Country(**country_data)
            db.add(db_country)
            db.commit()
            db.refresh(db_country)
            return {
                "success": True, 
                "message": "Country created successfully",
                "country": db_country
            }
    
    @staticmethod
    def delete_country(db: Session, country_id: int) -> Dict[str, Any]:
        db_country = db.query(Country).filter(Country.Id == country_id).first()
        if not db_country:
            return {"success": False, "message": "Country not found"}
        
        db.delete(db_country)
        db.commit()
        return {"success": True, "message": "Country deleted successfully"}
    
    @staticmethod
    def create_country(db: Session, country: CountryCreate) -> Country:
        if CountryService.check_country_exists(db, country.Name, country.Code):
            raise ValueError("Country with same name or code already exists")
        
        db_country = Country(**country.model_dump(exclude_none=True))
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country
    
    @staticmethod
    def update_country(db: Session, country_id: int, country: CountryUpdate) -> Optional[Country]:
        db_country = db.query(Country).filter(Country.Id == country_id).first()
        if db_country:
            update_data = country.model_dump(exclude_none=True)
            name = update_data.get('Name')
            code = update_data.get('Code')
            
            if name or code:
                if CountryService.check_country_exists(db, name, code, country_id):
                    raise ValueError("Country with same name or code already exists")
            
            for key, value in update_data.items():
                setattr(db_country, key, value)
            db.commit()
            db.refresh(db_country)
        return db_country
    
    @staticmethod
    def toggle_active_status(db: Session, country_id: int, is_active: bool) -> Optional[Country]:
        db_country = db.query(Country).filter(Country.Id == country_id).first()
        if db_country:
            db_country.IsActive = is_active
            db.commit()
            db.refresh(db_country)
        return db_country
    
    @staticmethod
    def search_countries(db: Session, search_term: str, limit: int = 10) -> List[Country]:
        search_pattern = f"%{search_term}%"
        return db.query(Country).filter(
            or_(
                func.coalesce(Country.Name, '').ilike(search_pattern),
                func.coalesce(Country.Code, '').ilike(search_pattern)
            )
        ).order_by(Country.Name).limit(limit).all()
    
    @staticmethod
    def get_countries_by_ids(db: Session, country_ids: List[int]) -> List[Country]:
        return db.query(Country).filter(Country.Id.in_(country_ids)).all()