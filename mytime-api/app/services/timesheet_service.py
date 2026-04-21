from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.time_sheet import Timesheet
from app.models.timesheet_task import TimesheetTask
from app.schemas.timesheet_schemas import TimesheetCreate, TimesheetUpdate


class TimesheetService:

    # ✅ 1. GET TIMESHEET (HEADER)
    @staticmethod
    def fetch_timesheet(db: Session, timesheet_id: int) -> Optional[Timesheet]:
        return db.query(Timesheet)\
               .filter(Timesheet.Id == timesheet_id)\
               .first()

    # ✅ 2. GET TASKS (TABLE)
    @staticmethod
    def fetch_timesheet_tasks(db: Session, timesheet_id: int):
        return db.query(TimesheetTask)\
               .filter(TimesheetTask.TimesheetId == timesheet_id)\
               .all()

    # ✅ 3. ALL TIMESHEETS
    @staticmethod
    def fetch_all_timesheets(db: Session) -> List[Timesheet]:
        return db.query(Timesheet)\
               .order_by(Timesheet.CreatedOn.desc())\
               .all()

    # ✅ 4. ALL TIMESHEETS (WITH TASKS - optional future use)
    @staticmethod
    def fetch_all_timesheets_with_tasks(db: Session) -> List[Timesheet]:
        return db.query(Timesheet)\
               .order_by(Timesheet.CreatedOn.desc())\
               .all()

    # ✅ 5. BY EMPLOYEE
    @staticmethod
    def get_timesheets_by_employee(db: Session, employee_id: int) -> List[Timesheet]:
        return db.query(Timesheet)\
               .filter(Timesheet.EmployeeId == employee_id)\
               .order_by(Timesheet.CreatedOn.desc())\
               .all()

    # ✅ 6. PAGINATION + FILTER
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

        sort_column = getattr(Timesheet, sort_by, Timesheet.Id)

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        items = query.offset(skip).limit(limit).all()

        return items, total

    # ✅ 7. INSERT / UPDATE TIMESHEET + TASKS
    @staticmethod
    def insert_or_update_timesheet(db: Session, timesheet_data: dict) -> Dict[str, Any]:

        valid_fields = {
            'Id', 'FromDate', 'ToDate', 'Description', 'EmployeeId',
            'UserId', 'Status', 'AssignedOn', 'AssignedTo', 'ApprovedOn',
            'ApprovedBy', 'ApprovedComments', 'CancelledOn', 'CancelledBy',
            'CancelledComments', 'RejectedOn', 'RejectedBy', 'RejectedComments',
            'CreatedBy', 'CreatedOn', 'ModifiedBy', 'ModifiedOn', 'IsActive', 'TotalHrs'
        }

        tasks_data = timesheet_data.pop('tasks', [])
        timesheet_id = timesheet_data.get('Id')

        filtered_data = {k: v for k, v in timesheet_data.items() if k in valid_fields}

        for key in filtered_data:
            if filtered_data[key] == "":
                filtered_data[key] = None

        # 🔹 UPDATE
        if timesheet_id:
            db_timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()

            if not db_timesheet:
                return {"success": False, "message": "Timesheet not found"}

            for key, value in filtered_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_timesheet, key, value)

            # TASKS
            for task in tasks_data:
                task_id = task.get('Id')

                if task_id:
                    db_task = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()
                    if db_task:
                        for k, v in task.items():
                            if k != 'Id' and v not in [None, ""]:
                                setattr(db_task, k, v)
                else:
                    task.pop('Id', None)
                    db.add(TimesheetTask(**task, TimesheetId=timesheet_id))

            db.commit()
            db.refresh(db_timesheet)

            return {"success": True, "message": "Updated", "timesheet": db_timesheet}

        # 🔹 CREATE
        filtered_data.pop('Id', None)
        filtered_data.setdefault('CreatedOn', datetime.utcnow())
        filtered_data.setdefault('IsActive', True)

        db_timesheet = Timesheet(**filtered_data)
        db.add(db_timesheet)
        db.flush()

        for task in tasks_data:
            task.pop('Id', None)
            db.add(TimesheetTask(**task, TimesheetId=db_timesheet.Id))

        db.commit()
        db.refresh(db_timesheet)

        return {"success": True, "message": "Created", "timesheet": db_timesheet}

    # ✅ 8. DELETE TIMESHEET
    @staticmethod
    def delete_timesheet(db: Session, timesheet_id: int):
        obj = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
        if not obj:
            return {"success": False, "message": "Not found"}

        db.delete(obj)
        db.commit()
        return {"success": True}

    # ✅ 9. DELETE TASK
    @staticmethod
    def delete_timesheet_task(db: Session, task_id: int):
        obj = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()
        if not obj:
            return {"success": False, "message": "Not found"}

        db.delete(obj)
        db.commit()
        return {"success": True}

    # ✅ 10. ADD TASK (FIXED VERSION)
    @staticmethod
    def add_timesheet_task(db: Session, timesheet_id: int, task_data: dict):
        # Check if timesheet exists
        timesheet = db.query(Timesheet).filter(Timesheet.Id == timesheet_id).first()
        if not timesheet:
            return None
        
        # Remove Id if present (let DB auto-generate)
        task_data.pop('Id', None)
        
        # Clean empty values
        clean_data = {k: v for k, v in task_data.items() if v not in [None, ""]}
        
        new_task = TimesheetTask(**clean_data, TimesheetId=timesheet_id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    # ✅ 11. UPDATE TASK
    @staticmethod
    def update_timesheet_task(db: Session, task_id: int, task_data: dict):
        task = db.query(TimesheetTask).filter(TimesheetTask.Id == task_id).first()

        if not task:
            return None

        for key, value in task_data.items():
            if value not in [None, ""]:
                setattr(task, key, value)

        db.commit()
        db.refresh(task)

        return task