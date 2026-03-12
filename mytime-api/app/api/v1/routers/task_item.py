from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.task_item_schemas import (
    TaskItemCreate,TaskItemUpdate,TaskItemResponse,TaskItemListResponse,
    TaskItemExistsResponse,TaskItemDeleteResponse    
)
from app.core.database import get_db
from app.services.task_item_service import TaskItemService
router = APIRouter()


@router.get("/fetchTaskItem/{taskitem_id}", response_model=TaskItemResponse)
async def fetch_task_item(taskitem_id: int, db: Session = Depends(get_db)):
    """Get TaskItem by ID"""
    try:
        taskitem = TaskItemService.fetch_task_item(db, taskitem_id)
        if not taskitem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TaskItem with ID {taskitem_id} not found"
            )
        return taskitem
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching TaskItem: {str(e)}"
        )
    
@router.get("/fetchAllTaskItems", response_model=List[TaskItemListResponse])
async def fetch_all_task_items(db: Session = Depends(get_db)):
    """Get all taskitems"""
    try:
        taskitems = TaskItemService.fetch_all_task_items(db)
        return taskitems
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching taskitems: {str(e)}"
        )
    
@router.post("/InsertOrUpdateTaskItem")
async def insert_or_update_task_item(TaskItem: dict, db: Session = Depends(get_db)):
    """Insert or update TaskItem"""
    try:
        response = TaskItemService.insert_or_update_task_item(db, TaskItem)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving designation: {str(e)}"
        )
    
@router.delete("/DeleteTaskItem/{taskitem_id}", response_model=TaskItemDeleteResponse)
async def delete_taskitem(taskitem_id: int, db: Session = Depends(get_db)):
    """Delete TaskItem"""
    try:
        response = TaskItemService.delete_taskitem(db, taskitem_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting taskitem: {str(e)}"
        )