from sqlalchemy import Boolean, Column, DateTime, Text, BigInteger, Date,Time,String,func,DECIMAL
from app.core.database import Base

class Attendance(Base):
    __tablename__    = "Attendance"

    AttendanceId     = Column(BigInteger, primary_key=True, index=True)
    EmployeeId       = Column(BigInteger, nullable=False)
    AttendanceDate   = Column(Date, nullable=False)
    CheckInTime      = Column(Time, nullable=True)
    CheckOutTime     = Column(Time, nullable=True)
    Status           = Column(String(20), nullable=False)
    WorkHours        = Column(DECIMAL(5,2), nullable=True)
    Description      = Column(String(255), nullable=True)

    CreatedOn        = Column(DateTime, nullable=True)
    CreatedBy        = Column(BigInteger, nullable=True)
    ModifiedOn       = Column(DateTime, nullable=True)
    ModifiedBy       = Column(BigInteger, nullable=True)

    def __repr__(self):
        return (
            f"<EmployeeAttendance("
            f"AttendanceId={self.AttendanceId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"Date={self.AttendanceDate}, "
            f"Status='{self.Status}', "
            f"WorkHours={self.WorkHours}"
            f")>"
        )