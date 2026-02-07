from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.state import State
from app.schemas.state_schemas import StateCreate, StateUpdate

class StateService:
    """Service for State operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_state(db: Session, state_id: int) -> Optional[State]:
        """Get state by ID - matches fetchState in C#"""
        return db.query(State).filter(State.StateId == state_id).first()
    
    @staticmethod
    def fetch_all_states(db: Session) -> List[State]:
        """Get all states - matches fetchAllStates in C#"""
        return db.query(State).all()
    
    @staticmethod
    def get_states_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        country_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "StateId",
        sort_order: str = "desc"
    ) -> Tuple[List[State], int]:
        """Get paginated states with filtering and sorting"""
        query = db.query(State)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(State.Name, '').ilike(search_term),
                    func.coalesce(State.StateCode, '').ilike(search_term),
                    func.coalesce(State.CountryCode, '').ilike(search_term),
                    func.coalesce(State.Description, '').ilike(search_term)
                )
            )
        
        # Apply country filter
        if country_id is not None:
            query = query.filter(State.CountryId == country_id)
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(State.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(State, sort_by)
        except AttributeError:
            # Default to StateId if sort_by column doesn't exist
            sort_column = State.StateId
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def get_states_by_country(db: Session, country_id: int) -> List[State]:
        """Get all states for a specific country"""
        return db.query(State).filter(
            State.CountryId == country_id,
            State.IsActive == True
        ).order_by(State.Name).all()
    
    @staticmethod
    def check_state_exists(db: Session, state_name: str, country_id: int, exclude_id: Optional[int] = None) -> bool:
        """Check if a state with the same name exists in the same country"""
        query = db.query(State).filter(
            State.Name == state_name,
            State.CountryId == country_id
        )
        
        if exclude_id:
            query = query.filter(State.StateId != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def insert_or_update_state(db: Session, state_data: dict) -> Dict[str, Any]:
        """Insert or update state - matches InsertOrUpdateState in C#"""
        state_id = state_data.get('StateId')
        
        if state_id:
            # Update existing state
            db_state = db.query(State).filter(State.StateId == state_id).first()
            if not db_state:
                return {"success": False, "message": "State not found", "state": None}
            
            # Check for duplicate name if name is being updated
            if 'Name' in state_data and state_data['Name'] != db_state.Name:
                if StateService.check_state_exists(db, state_data['Name'], db_state.CountryId, state_id):
                    return {
                        "success": False, 
                        "message": f"State with name '{state_data['Name']}' already exists in this country",
                        "state": None
                    }
            
            for key, value in state_data.items():
                if key != 'StateId' and value is not None:
                    setattr(db_state, key, value)
            
            db.commit()
            db.refresh(db_state)
            return {
                "success": True, 
                "message": "State updated successfully",
                "state": db_state
            }
        else:
            # Create new state
            # Check for duplicate name
            if StateService.check_state_exists(db, state_data['Name'], state_data['CountryId']):
                return {
                    "success": False, 
                    "message": f"State with name '{state_data['Name']}' already exists in this country",
                    "state": None
                }
            
            # Remove StateId if present in create mode
            state_data.pop('StateId', None)
            db_state = State(**state_data)
            db.add(db_state)
            db.commit()
            db.refresh(db_state)
            return {
                "success": True, 
                "message": "State created successfully",
                "state": db_state
            }
    
    @staticmethod
    def delete_state(db: Session, state_id: int) -> Dict[str, Any]:
        """Delete state - matches DeleteState in C#"""
        db_state = db.query(State).filter(State.StateId == state_id).first()
        if not db_state:
            return {"success": False, "message": "State not found"}
        
        db.delete(db_state)
        db.commit()
        return {"success": True, "message": "State deleted successfully"}
    
    @staticmethod
    def create_state(db: Session, state: StateCreate) -> State:
        """Create new state"""
        # Check for duplicate name
        if StateService.check_state_exists(db, state.Name, state.CountryId):
            raise ValueError(f"State with name '{state.Name}' already exists in this country")
        
        db_state = State(**state.model_dump(exclude_none=True))
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
        return db_state
    
    @staticmethod
    def update_state(db: Session, state_id: int, state: StateUpdate) -> Optional[State]:
        """Update existing state"""
        db_state = db.query(State).filter(State.StateId == state_id).first()
        if db_state:
            # Check for duplicate name if name is being updated
            update_data = state.model_dump(exclude_none=True)
            if 'Name' in update_data and update_data['Name'] != db_state.Name:
                country_id = update_data.get('CountryId', db_state.CountryId)
                if StateService.check_state_exists(db, update_data['Name'], country_id, state_id):
                    raise ValueError(f"State with name '{update_data['Name']}' already exists in this country")
            
            for key, value in update_data.items():
                setattr(db_state, key, value)
            db.commit()
            db.refresh(db_state)
        return db_state
    
    @staticmethod
    def toggle_active_status(db: Session, state_id: int, is_active: bool) -> Optional[State]:
        """Toggle the active status of a state"""
        db_state = db.query(State).filter(State.StateId == state_id).first()
        if db_state:
            db_state.IsActive = is_active
            db.commit()
            db.refresh(db_state)
        return db_state
    
    @staticmethod
    def get_states_by_country_code(db: Session, country_code: str) -> List[State]:
        """Get states by country code"""
        return db.query(State).filter(
            State.CountryCode == country_code,
            State.IsActive == True
        ).order_by(State.Name).all()
    
    @staticmethod
    def get_state_by_code(db: Session, state_code: str, country_code: Optional[str] = None) -> Optional[State]:
        """Get state by state code (optionally filtered by country code)"""
        query = db.query(State).filter(State.StateCode == state_code)
        
        if country_code:
            query = query.filter(State.CountryCode == country_code)
        
        return query.first()