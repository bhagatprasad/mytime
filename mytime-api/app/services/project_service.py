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
        return db.query(Project).filter(Project.IsActive == True).all()

    @staticmethod
    def insert_or_update_project(db: Session, project_data: dict) -> Dict[str, Any]:
        """Insert or update project - matches InsertOrUpdatProject in C#"""
        project_id = project_data.get('ProjectId')
        
        if project_id:
            # Update existing project
            db_project = db.query(Project).filter(Project.ProjectId == project_id).first()
            if not db_project:
                return {"success": False, "message": "Project not found", "project": None}
            
            for key, value in project_data.items():
                if key != 'ProjectId' and value is not None:
                    setattr(db_project, key, value)
            
            db.commit()
            db.refresh(db_project)
            return {
                "success": True, 
                "message": "Project updated successfully",
                "project": db_project
            }
        else:
           
            project_data.pop('ProjectId', None)
            db_project = Project(**project_data)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return {
                "success": True, 
                "message": "Project created successfully",
                "project": db_project
            }
        
    @staticmethod
    def delete_project(db: Session, project_id: int) -> Dict[str, Any]:
        """Delete project - matches DeleteProject in C#"""
        db_project = db.query(Project).filter(Project.ProjectId == project_id).first()
        if not db_project:
            return {"success": False, "message": "Project not found"}
        
        db.delete(db_project)
        db.commit()
        return {"success": True, "message": "Project deleted successfully"}
    
