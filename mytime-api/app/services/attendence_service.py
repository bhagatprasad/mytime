from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, date, time
import re

from app.models.attendence import Attendence
from app.schemas.attendence_schemas import AttendenceCreate, AttendenceUpdate


class AttendenceService:
    """Service for Attendence operations"""

    @staticmethod
    def fetch_attendence(db: Session, attendence_id: int) -> Optional[Attendence]:
        return db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()
    
    @staticmethod
    def fetch_attendence_by_employee(db: Session, employee_id: int) -> List[Attendence]:
        return db.query(Attendence).filter(Attendence.EmployeeId == employee_id).order_by(
            Attendence.AttendenceDate.desc()
        ).all()

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
    def exists(db: Session, attendence_id: int) -> bool:
        """Check if attendence exists"""
        return db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first() is not None

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
    def _parse_datetime(value):
        """Helper method to convert various datetime string formats to datetime object"""
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value
            
        if isinstance(value, str):
            # Handle format like "Thu Mar 26 2026"
            try:
                # Try parsing with different formats
                formats = [
                    '%a %b %d %Y',           # Thu Mar 26 2026
                    '%Y-%m-%d',               # 2026-03-26
                    '%Y-%m-%d %H:%M:%S',      # 2026-03-26 10:30:00
                    '%Y-%m-%dT%H:%M:%S',      # 2026-03-26T10:30:00
                    '%Y-%m-%dT%H:%M:%S.%fZ',  # 2026-03-26T10:30:00.000Z
                ]
                for fmt in formats:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
            except:
                pass
        return None

    @staticmethod
    def _convert_time(value):
        """Helper method to convert string time to time object"""
        if value is None or value == "":
            return None
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            try:
                # Handle time format like "11:26"
                parts = value.split(':')
                if len(parts) == 2:
                    return time(hour=int(parts[0]), minute=int(parts[1]))
                elif len(parts) == 3:
                    return time(hour=int(parts[0]), minute=int(parts[1]), second=int(parts[2]))
            except:
                pass
        return None

    @staticmethod
    def _convert_date(value):
        """Helper method to convert string date to date object"""
        if value is None or value == "":
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                # Handle format like "2026-03-24T00:00:00.000Z"
                if 'T' in value:
                    return date.fromisoformat(value.split('T')[0])
                else:
                    return date.fromisoformat(value)
            except:
                pass
        return None

    # (INSERT + UPDATE)
    @staticmethod
    def insert_or_update_attendence(
        db: Session,
        attendence_data: dict
    ) -> Dict[str, Any]:

        attendence_id = attendence_data.get("AttendenceId")
        
        # Define valid fields for Attendence model
        valid_fields = {
            'AttendenceId', 'EmployeeId', 'AttendenceDate', 'CheckInTime', 
            'CheckOutTime', 'Status', 'WorkHours', 'Description', 
            'ApprovalStatus', 'ApprovedBy', 'ApprovedOn', 'RejectedBy', 
            'RejectedOn', 'RejectionReason', 'CreatedOn', 'CreatedBy', 
            'ModifiedOn', 'ModifiedBy', 'WorkType'
        }
        
        # Filter and process the data
        processed_data = {}
        for key, value in attendence_data.items():
            if key in valid_fields and value is not None and value != "":
                # Handle time fields
                if key in ['CheckInTime', 'CheckOutTime', 'WorkHours']:
                    converted = AttendenceService._convert_time(value)
                    if converted:
                        processed_data[key] = converted
                # Handle date fields
                elif key == 'AttendenceDate':
                    converted = AttendenceService._convert_date(value)
                    if converted:
                        processed_data[key] = converted
                # Handle datetime fields
                elif key in ['CreatedOn', 'ModifiedOn', 'ApprovedOn', 'RejectedOn']:
                    converted = AttendenceService._parse_datetime(value)
                    if converted:
                        processed_data[key] = converted
                # Handle all other fields
                else:
                    processed_data[key] = value

        # UPDATE
        if attendence_id and attendence_id != 0:
            db_attendence = db.query(Attendence).filter(
                Attendence.AttendenceId == attendence_id
            ).first()

            if not db_attendence:
                return {"success": False, "message": "Attendence not found"}

            # Check for duplicate (if date or employee changed)
            emp_id = processed_data.get('EmployeeId', db_attendence.EmployeeId)
            att_date = processed_data.get('AttendenceDate', db_attendence.AttendenceDate)
            
            # Only check if either employee or date changed
            if processed_data.get('EmployeeId') or processed_data.get('AttendenceDate'):
                if AttendenceService.check_attendence_exists(db, emp_id, att_date, attendence_id):
                    return {"success": False, "message": "Attendence already exists for this employee on this date"}

            # Update fields
            for key, value in processed_data.items():
                if key != 'AttendenceId':
                    setattr(db_attendence, key, value)

            # Update ModifiedOn
            db_attendence.ModifiedOn = datetime.now()

            db.commit()
            db.refresh(db_attendence)

            return {
                "success": True,
                "message": "Attendence updated successfully",
                "data": db_attendence
            }

        # CREATE
        else:
            # Check for duplicate
            emp_id = processed_data.get('EmployeeId')
            att_date = processed_data.get('AttendenceDate')
            
            if not emp_id or not att_date:
                return {"success": False, "message": "EmployeeId and AttendenceDate are required"}
            
            if AttendenceService.check_attendence_exists(db, emp_id, att_date):
                return {"success": False, "message": "Attendence already exists for this employee on this date"}

            # Remove AttendenceId if present
            processed_data.pop('AttendenceId', None)
            
            # Set CreatedOn if not provided or invalid
            if 'CreatedOn' not in processed_data or processed_data['CreatedOn'] is None:
                processed_data['CreatedOn'] = datetime.now()
            
            # Set default values
            if 'ApprovalStatus' not in processed_data or processed_data['ApprovalStatus'] is None:
                processed_data['ApprovalStatus'] = 'Pending'
            if 'WorkType' not in processed_data or processed_data['WorkType'] is None:
                processed_data['WorkType'] = 'Office'
            if 'Status' not in processed_data or processed_data['Status'] is None:
                processed_data['Status'] = 'Present'
            if 'CheckInTime' not in processed_data:
                processed_data['CheckInTime'] = None
            if 'CheckOutTime' not in processed_data:
                processed_data['CheckOutTime'] = None
            if 'WorkHours' not in processed_data:
                processed_data['WorkHours'] = None

            db_attendence = Attendence(**processed_data)

            db.add(db_attendence)
            db.commit()
            db.refresh(db_attendence)

            return {
                "success": True,
                "message": "Attendence created successfully",
                "data": db_attendence
            }

    @staticmethod
    def delete_attendence(db: Session, attendence_id: int) -> tuple:
        """Delete attendence record"""
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if not db_attendence:
            return False, "Attendence not found"

        db.delete(db_attendence)
        db.commit()

        return True, "Attendence deleted successfully"

    @staticmethod
    def approve_attendence(db: Session, attendence_id: int, user_id: int) -> Optional[Attendence]:
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if db_attendence:
            db_attendence.ApprovalStatus = "Approved"
            db_attendence.ApprovedBy = user_id
            db_attendence.ApprovedOn = datetime.now()
            db.commit()
            db.refresh(db_attendence)

        return db_attendence

    @staticmethod
    def reject_attendence(db: Session, attendence_id: int, user_id: int, reason: str) -> Optional[Attendence]:
        db_attendence = db.query(Attendence).filter(
            Attendence.AttendenceId == attendence_id
        ).first()

        if db_attendence:
            db_attendence.ApprovalStatus = "Rejected"
            db_attendence.RejectedBy = user_id
            db_attendence.RejectedOn = datetime.now()
            db_attendence.RejectionReason = reason
            db.commit()
            db.refresh(db_attendence)

        return db_attendence

    @staticmethod
    def get_today_attendence(db: Session, employee_id: int) -> Optional[Attendence]:
        """Get today's attendence for an employee"""
        today = date.today()
        return db.query(Attendence).filter(
            Attendence.EmployeeId == employee_id,
            Attendence.AttendenceDate == today
        ).first()

    @staticmethod
    def get_attendence_by_date_range(
        db: Session,
        employee_id: int,
        from_date: date,
        to_date: date
    ) -> List[Attendence]:
        """Get attendence records for an employee within a date range"""
        return db.query(Attendence).filter(
            Attendence.EmployeeId == employee_id,
            Attendence.AttendenceDate >= from_date,
            Attendence.AttendenceDate <= to_date
        ).order_by(Attendence.AttendenceDate.asc()).all()

    @staticmethod
    def get_pending_approvals(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[Attendence], int]:
        """Get all pending approval attendence records"""
        query = db.query(Attendence).filter(Attendence.ApprovalStatus == "Pending")
        total = query.count()
        items = query.offset(skip).limit(limit).order_by(Attendence.AttendenceDate.desc()).all()
        return items, total