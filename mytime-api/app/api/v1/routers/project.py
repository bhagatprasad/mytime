from fastapi import APIRouter, Depends, HTTPException,status,Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.project_service import ProjectService
from app.schemas.project_schemas import (
    ProjectResponse,
    ProjectListResponse,ProjectDeleteResponse
)

router = APIRouter()
#router = APIRouter(prefix="/projects", tags=["Projects"])


# Get project by ID
@router.get("/{project_id}", response_model=ProjectResponse)
def fetch_project_details(project_id: int, db: Session = Depends(get_db)):
    project = ProjectService.fetch_project_details(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


# Get all projects
@router.get("/", response_model=ProjectListResponse)
def fetch_all_project_details(db: Session = Depends(get_db)):

    projects = ProjectService.fetch_all_project_details(db)

    return {
        "total": len(projects),
        "items": projects,
        "page": 1,
        "size": len(projects),
        "pages": 1
    }

#insert or update project
@router.post("/InsertOrUpdateProject")
async def insert_or_update_project(project: dict, db: Session = Depends(get_db)):
    """Insert or update project - matches C# InsertOrUpdateProject endpoint"""
    try:
        response = ProjectService.insert_or_update_project(db, project)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.delete("/DeleteProject/{project_id}", response_model=ProjectDeleteResponse)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete project - matches C# DeleteProject endpoint"""
    try:
        response = ProjectService.delete_project(db, project_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )