from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.attendence import Attendence
from app.schemas.attendence_schemas import AttendenceCreate, AttendenceUpdate,AttendenceCreate


class AttendenceService:
    """Service for Attendence operations"""

    @staticmethod
    def fetch_attendence(db: Session, attendence_id: int) -> Optional[Attendence]:
        return db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

    @staticmethod
    def fetch_all_attendence(db: Session) -> List[Attendence]:
        return db.query(Attendence).order_by(
            Attendence.AttendenceDate.desc()
        ).all()

    @staticmethod
    def get_attendence_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        approval_status: Optional[str] = None,
        sort_by: str = "AttendenceId",
        sort_order: str = "desc"
    ) -> Tuple[List[Attendence], int]:

        query = db.query(Attendence)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Attendence.Description, '').ilike(search_term),
                    func.coalesce(Attendence.Status, '').ilike(search_term)
                )
            )

        if employee_id:
            query = query.filter(Attendence.EmployeeId == employee_id)

        if status:
            query = query.filter(Attendence.Status == status)

        if approval_status:
            query = query.filter(Attendence.ApprovalStatus == approval_status)

        total = query.count()

        sort_column = getattr(Attendence, sort_by, Attendence.AttendenceId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        items = query.offset(skip).limit(limit).all()

        return items, total

    @staticmethod
    def check_attendence_exists(
        db: Session,
        employee_id: int,
        attendence_date,
        exclude_id: Optional[int] = None
    ) -> bool:

        query = db.query(Attendence).filter(
            Attendence.EmployeeId == employee_id,
            Attendence.AttendenceDate == attendence_date
        )

        if exclude_id:
            query = query.filter(Attendence.AttendenceId != exclude_id)

        return query.first() is not None

    @staticmethod
    def create_attendence(db: Session, attendence: AttendenceCreate) -> Attendence:

        if AttendenceService.check_attendence_exists(
            db, attendence.EmployeeId, attendence.AttendenceDate
        ):
            raise ValueError("Attendence already exists for this employee on this date")

        db_attendence = Attendence(**attendence.dict(exclude_none=True))
        db.add(db_attendence)
        db.commit()
        db.refresh(db_attendence)
        return db_attendence

    @staticmethod
    def update_attendence(
        db: Session,
        attendence_id: int,
        attendence: AttendenceUpdate
    ) -> Optional[Attendence]:

        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if db_attendence:
            update_data = attendence.dict(exclude_none=True)

            emp_id = update_data.get('EmployeeId', db_attendence.EmployeeId)
            date = update_data.get('AttendenceDate', db_attendence.AttendenceDate)

            if AttendenceService.check_attendence_exists(db, emp_id, date, attendence_id):
                raise ValueError("Attendence already exists for this employee on this date")

            for key, value in update_data.items():
                setattr(db_attendence, key, value)

            db.commit()
            db.refresh(db_attendence)

        return db_attendence

    @staticmethod
    def delete_attendence(db: Session, attendence_id: int) -> Dict[str, Any]:
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if not db_attendence:
            return {"success": False, "message": "Attendence not found"}

        db.delete(db_attendence)
        db.commit()

        return {"success": True, "message": "Attendence deleted successfully"}

    @staticmethod
    def approve_attendence(db: Session, attendence_id: int, user_id: int):
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if db_attendence:
            db_attendence.ApprovalStatus = "Approved"
            db_attendence.ApprovedBy = user_id
            db_attendence.ApprovedOn = func.now()
            db.commit()
            db.refresh(db_attendence)

        return db_attendence

    @staticmethod
    def reject_attendence(db: Session, attendence_id: int, user_id: int, reason: str):
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if db_attendence:
            db_attendence.ApprovalStatus = "Rejected"
            db_attendence.RejectedBy = user_id
            db_attendence.RejectedOn = func.now()
            db_attendence.RejectionReason = reason
            db.commit()
            db.refresh(db_attendence)

        return db_attendence