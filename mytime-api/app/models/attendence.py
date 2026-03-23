from sqlalchemy import Column, DateTime, BigInteger, Date, Time, String, DECIMAL, func
from app.core.database import Base

class Attendence(Base):
    __tablename__ = "Attendence"

    AttendenceId   = Column(BigInteger, primary_key=True, index=True)
    EmployeeId     = Column(BigInteger, nullable=False)
    AttendenceDate = Column(Date, nullable=False)

    CheckInTime    = Column(Time, nullable=True)
    CheckOutTime   = Column(Time, nullable=True)

    Status         = Column(String(20), nullable=False)
    WorkHours      = Column(DECIMAL(5, 2), nullable=True)
    Description    = Column(String(255), nullable=True)

    ApprovalStatus = Column(String(20), nullable=True, default="Pending")
    ApprovedBy     = Column(BigInteger, nullable=True)
    ApprovedOn     = Column(DateTime, nullable=True)
    RejectedBy     = Column(BigInteger, nullable=True)
    RejectedOn     = Column(DateTime, nullable=True)
    RejectionReason = Column(String(255), nullable=True)

    CreatedOn      = Column(DateTime, nullable=False, server_default=func.now())
    CreatedBy      = Column(BigInteger, nullable=True)
    ModifiedOn     = Column(DateTime, nullable=True, onupdate=func.now())
    ModifiedBy     = Column(BigInteger, nullable=True)
    WorkType       = Column(String(50), nullable=False, default='Office')

    def __repr__(self):
        return (
            f"<Attendence("
            f"AttendenceId={self.AttendenceId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"Date={self.AttendenceDate}, "
            f"Status='{self.Status}', "
            f"WorkHours={self.WorkHours}"
            f")>"
        )