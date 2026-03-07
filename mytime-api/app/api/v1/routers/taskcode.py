from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.taskcode_schemas import (
    TaskcodeResponse,
    TaskcodeDeleteResponse,
    TaskcodeCreate
)

from app.core.database import get_db
from app.services.taskcode_service import TaskcodeService

router = APIRouter()


# Fetch single taskcode
@router.get("/fetchtaskcode/{taskcode_id}", response_model=TaskcodeResponse)
async def fetch_taskcode(taskcode_id: int, db: Session = Depends(get_db)):
    try:
        taskcode = TaskcodeService.fetch_taskcode(db, taskcode_id)

        if not taskcode:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TaskCode with ID {taskcode_id} not found"
            )

        return taskcode

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching TaskCode: {str(e)}"
        )


# Fetch all

@router.get("/fetchAllTaskcodes", response_model=List[TaskcodeResponse])
async def fetch_all_taskcodes(db: Session = Depends(get_db)):
    try:
        taskcodes = TaskcodeService.fetch_all_taskcodes(db)
        return taskcodes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching taskcodes: {str(e)}"
        )

@router.post("/InsertOrUpdateTaskcode")
async def insert_or_update_taskcode(
    taskcode: TaskcodeResponse,
    db: Session = Depends(get_db)
):
    response = TaskcodeService.insert_or_update_taskcode(
        db, taskcode.dict()
    )
    return response

# Delete
@router.delete("/DeleteTaskcode/{taskcode_id}", response_model=TaskcodeDeleteResponse)
async def delete_taskcode(taskcode_id: int, db: Session = Depends(get_db)):
    try:
        response = TaskcodeService.delete_taskcode(db, taskcode_id)

        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting TaskCode: {str(e)}"
        )