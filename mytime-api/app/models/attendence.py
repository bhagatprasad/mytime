from sqlalchemy import Column, BigInteger, Date, Time, String, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Attendance(Base):
    __tablename__ = "EmployeeAttendance"

    AttendanceId = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    EmployeeId = Column(BigInteger, nullable=False)
    AttendanceDate = Column(Date, nullable=False)

    CheckInTime = Column(Time, nullable=True)
    CheckOutTime = Column(Time, nullable=True)

    Status = Column(String(20), nullable=False)
    WorkHours = Column(DECIMAL(5, 2), nullable=True)
    Description = Column(String(255), nullable=True)

    # Audit Fields
    CreatedOn = Column(DateTime, server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime, nullable=True, onupdate=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)

    # Approval Workflow
    ApprovalStatus = Column(String(20), default="Pending")
    ApprovedBy = Column(BigInteger, nullable=True)
    ApprovedOn = Column(DateTime, nullable=True)

    RejectedBy = Column(BigInteger, nullable=True)
    RejectedOn = Column(DateTime, nullable=True)
    RejectionReason = Column(String(255), nullable=True)

    def __repr__(self):
        return (
            f"<EmployeeAttendance("
            f"AttendanceId={self.AttendanceId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"Date={self.AttendanceDate}, "
            f"Status={self.Status}, "
            f"ApprovalStatus={self.ApprovalStatus}"
            f")>"
        )