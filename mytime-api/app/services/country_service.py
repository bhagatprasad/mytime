from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from app.models.country import Country


class CountryService:
    """Country service starts"""
    @staticmethod
    def fetch_all_countries(db:Session) -> List[Country]:
        """fetchig countries from database"""
        return db.query(Country).all()
