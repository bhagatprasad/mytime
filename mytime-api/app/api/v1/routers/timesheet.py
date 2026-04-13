from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.timesheet_schemas import (
    TimesheetResponse,
    TimesheetListResponse,
    TimesheetDeleteResponse,
    TimesheetTaskResponse
)
from app.core.database import get_db
from app.services.timesheet_service import TimesheetService

router = APIRouter()

@router.get("/fetchTimesheet/{timesheet_id}", response_model=TimesheetResponse)
async def fetch_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    timesheet = TimesheetService.fetch_timesheet_with_tasks(db, timesheet_id)
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timesheet with ID {timesheet_id} not found"
        )
    return timesheet

@router.get("/fetchTimesheetWithTasks/{timesheet_id}", response_model=TimesheetResponse)
async def fetch_timesheet_with_tasks(timesheet_id: int, db: Session = Depends(get_db)):
    timesheet = TimesheetService.fetch_timesheet_with_tasks(db, timesheet_id)
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Timesheet with ID {timesheet_id} not found"
        )
    return timesheet

@router.get("/fetchAllTimesheets", response_model=List[TimesheetResponse])
async def fetch_all_timesheets(db: Session = Depends(get_db)):
    timesheets = TimesheetService.fetch_all_timesheets_with_tasks(db)
    return timesheets

@router.get("/getTimesheetsByEmployee/{employee_id}", response_model=List[TimesheetResponse])
async def get_timesheets_by_employee(employee_id: int, db: Session = Depends(get_db)):
    timesheets = TimesheetService.get_timesheets_by_employee(db, employee_id)
    return timesheets


@router.post("/InsertOrUpdateTimesheet")
async def insert_or_update_timesheet(timesheet: dict, db: Session = Depends(get_db)):
    response = TimesheetService.insert_or_update_timesheet(db, timesheet)
    if not response["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response["message"]
        )
    return response

@router.delete("/DeleteTimesheet/{timesheet_id}", response_model=TimesheetDeleteResponse)
async def delete_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    response = TimesheetService.delete_timesheet(db, timesheet_id)
    if not response["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )
    return response

@router.delete("/DeleteTimesheetTask/{task_id}")
async def delete_timesheet_task(task_id: int, db: Session = Depends(get_db)):
    response = TimesheetService.delete_timesheet_task(db, task_id)
    if not response["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=response["message"]
        )
    return response

# @router.post("/AddTimesheetTask/{timesheet_id}", response_model=TimesheetTaskResponse)
# async def add_timesheet_task(timesheet_id: int, task_data: dict, db: Session = Depends(get_db)):
#     task = TimesheetService.add_timesheet_task(db, timesheet_id, task_data)
#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Timesheet with ID {timesheet_id} not found"
#         )
#     return task

from fastapi import HTTPException, status

@router.post("/AddTimesheetTask/{timesheet_id}", response_model=TimesheetTaskResponse)
async def add_timesheet_task(timesheet_id: int, task_data: dict, db: Session = Depends(get_db)):
    try:
        task = TimesheetService.add_timesheet_task(db, timesheet_id, task_data)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Timesheet with ID {timesheet_id} not found"
            )

        return task

    except Exception as e:
        print("🔥 BACKEND ERROR:", str(e))   # 👈 VERY IMPORTANT
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.put("/UpdateTimesheetTask/{task_id}", response_model=TimesheetTaskResponse)
async def update_timesheet_task(task_id: int, task_data: dict, db: Session = Depends(get_db)):
    task = TimesheetService.update_timesheet_task(db, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.get("/get_timesheet_tasks/{timesheet_id}")
async def get_timesheet_tasks(timesheet_id: int, db: Session = Depends(get_db)):
    from app.models.timesheet_task import TimesheetTask
    
    tasks = db.query(TimesheetTask).filter(TimesheetTask.TimesheetId == timesheet_id).all()
    
    return tasks