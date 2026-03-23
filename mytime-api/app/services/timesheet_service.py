from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.time_sheet import Timesheet
from app.models.timesheet_task import TimesheetTask
from app.schemas.timesheet_schemas import TimesheetCreate, TimesheetUpdate

class TimesheetService:
    @staticmethod
    def fetch_timesheet(db: Session, timesheet_id: int) -> Optional[Timesheet]:
        return db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()

    @staticmethod
    def fetch_timesheet_with_tasks(db: Session, timesheet_id: int) -> Optional[Timesheet]:
        return db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()

    @staticmethod
    def fetch_all_timesheets(db: Session) -> List[Timesheet]:
        return db.query(Timesheet).order_by(Timesheet.CreatedOn.desc()).all()

    @staticmethod
    def fetch_all_timesheets_with_tasks(db: Session) -> List[Timesheet]:
        return db.query(Timesheet).order_by(Timesheet.CreatedOn.desc()).all()

    @staticmethod
    def get_timesheets_by_employee(db: Session, employee_id: int) -> List[Timesheet]:
        return db.query(Timesheet).filter(Timesheet.EmployeeId == employee_id).order_by(Timesheet.CreatedOn.desc()).all()

    @staticmethod
    def get_timesheets_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[Timesheet], int]:
        query = db.query(Timesheet)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Timesheet.Description, '').ilike(search_term),
                    func.coalesce(Timesheet.Status, '').ilike(search_term)
                )
            )

        if employee_id is not None:
            query = query.filter(Timesheet.EmployeeId == employee_id)

        if status is not None:
            query = query.filter(Timesheet.Status == status)

        if is_active is not None:
            query = query.filter(Timesheet.IsActive == is_active)

        if from_date is not None:
            query = query.filter(Timesheet.FromDate >= from_date)

        if to_date is not None:
            query = query.filter(Timesheet.ToDate <= to_date)

        total = query.count()

        try:
            sort_column = getattr(Timesheet, sort_by, Timesheet.Id)
        except AttributeError:
            sort_column = Timesheet.Id

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        items = query.offset(skip).limit(limit).all()

        return items, total

    @staticmethod
    def insert_or_update_timesheet(db: Session, timesheet_data: dict) -> Dict[str, Any]:
        timesheet_id = timesheet_data.get('Id')
        tasks_data = timesheet_data.pop('tasks', [])

        if timesheet_id:
            db_timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
            if not db_timesheet:
                return {"success": False, "message": "Timesheet not found", "timesheet": None}

            for key, value in timesheet_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_timesheet, key, value)

            if tasks_data:
                for task_data in tasks_data:
                    task_id = task_data.get('Id')
                    if task_id:
                        db_task = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()
                        if db_task and db_task.TimesheetId == timesheet_id:
                            for key, value in task_data.items():
                                if key != 'Id' and value is not None:
                                    setattr(db_task, key, value)
                    else:
                        new_task = TimesheetTask(**task_data, TimesheetId=timesheet_id)
                        db.add(new_task)

            db.commit()
            db.refresh(db_timesheet)
            return {"success": True, "message": "Timesheet updated successfully", "timesheet": db_timesheet}
        else:
            timesheet_data.pop('Id', None)
            db_timesheet = Timesheet(**timesheet_data)
            db.add(db_timesheet)
            db.flush()

            for task_data in tasks_data:
                task_data.pop('Id', None)
                new_task = TimesheetTask(**task_data, TimesheetId=db_timesheet.Id)
                db.add(new_task)

            db.commit()
            db.refresh(db_timesheet)
            return {"success": True, "message": "Timesheet created successfully", "timesheet": db_timesheet}

    @staticmethod
    def delete_timesheet(db: Session, timesheet_id: int) -> Dict[str, Any]:
        db_timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
        if not db_timesheet:
            return {"success": False, "message": "Timesheet not found"}

        db.delete(db_timesheet)
        db.commit()
        return {"success": True, "message": "Timesheet deleted successfully"}

    @staticmethod
    def delete_timesheet_task(db: Session, task_id: int) -> Dict[str, Any]:
        db_task = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()
        if not db_task:
            return {"success": False, "message": "Task not found"}

        db.delete(db_task)
        db.commit()
        return {"success": True, "message": "Task deleted successfully"}

    @staticmethod
    def create_timesheet(db: Session, timesheet: TimesheetCreate) -> Timesheet:
        db_timesheet = Timesheet(**timesheet.model_dump(exclude_none=True, exclude={'tasks'}))
        db.add(db_timesheet)
        db.flush()

        for task in timesheet.tasks:
            db_task = TimesheetTask(**task.model_dump(exclude_none=True), TimesheetId=db_timesheet.Id)
            db.add(db_task)

        db.commit()
        db.refresh(db_timesheet)
        return db_timesheet

    @staticmethod
    def update_timesheet(db: Session, timesheet_id: int, timesheet: TimesheetUpdate) -> Optional[Timesheet]:
        db_timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
        if db_timesheet:
            update_data = timesheet.model_dump(exclude_none=True)
            for key, value in update_data.items():
                setattr(db_timesheet, key, value)
            db.commit()
            db.refresh(db_timesheet)
        return db_timesheet

    @staticmethod
    def update_timesheet_task(db: Session, task_id: int, task_data: dict) -> Optional[TimesheetTask]:
        db_task = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()
        if db_task:
            for key, value in task_data.items():
                if value is not None:
                    setattr(db_task, key, value)
            db.commit()
            db.refresh(db_task)
        return db_task

    @staticmethod
    def add_timesheet_task(db: Session, timesheet_id: int, task_data: dict) -> Optional[TimesheetTask]:
        db_timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
        if not db_timesheet:
            return None

        new_task = TimesheetTask(**task_data, TimesheetId=timesheet_id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task