from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.project_service import ProjectService
from app.schemas.project_schemas import (
    ProjectResponse,
    ProjectListResponse
)

router = APIRouter()

@router.get("/{project_id}", response_model=ProjectResponse)
def fetch_project_details(project_id: int, db: Session = Depends(get_db)):
    project = ProjectService.fetch_project_details(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


# Get all projects
@router.get("/fetchallprojects", response_model=ProjectListResponse)
def fetch_all_project_details(db: Session = Depends(get_db)):

    projects = ProjectService.fetch_all_project_details(db)

    return {
        "total": len(projects),
        "items": projects,
        "page": 1,
        "size": len(projects),
        "pages": 1
    }