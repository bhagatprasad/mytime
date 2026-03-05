from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from app.models.project import Project

class ProjectService:
    """Service for Project operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_project_details(db: Session, project_id: int) -> Optional[Project]:
        """Get Project by ID - matches fetchprojectDetails in C#"""
        return db.query(Project).filter(Project.ProjectId == project_id).first()
    
    @staticmethod
    def fetch_all_project_details(db: Session) -> List[Project]:
        """Get all project details - matches fetchAllprojectdetails in C#"""
        return db.query(Project).all()
    
