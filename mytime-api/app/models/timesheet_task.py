from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TimesheetTask(Base):
    __tablename__ = "TimesheetTask"

    Id = Column(BigInteger, primary_key=True, index=True)

    TimesheetId = Column(BigInteger, ForeignKey("Timesheet.Id"), nullable=True)
    TaskItemId = Column(BigInteger, ForeignKey("TaskItem.TaskItemId"), nullable=True)
    TaskCodeId = Column(BigInteger, ForeignKey("TaskCode.TaskCodeId"), nullable=True)

    MondayHours = Column(BigInteger, nullable=True)
    TuesdayHours = Column(BigInteger, nullable=True)
    WednesdayHours = Column(BigInteger, nullable=True)
    ThursdayHours = Column(BigInteger, nullable=True)
    FridayHours = Column(BigInteger, nullable=True)
    SaturdayHours = Column(BigInteger, nullable=True)
    SundayHours = Column(BigInteger, nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, nullable=True)

    # Relationships
    timesheet = relationship("Timesheet", back_populates="timesheet_tasks")
    task_item = relationship("TaskItem")
    task_code = relationship("TaskCode")

    def __repr__(self):
        return (
            f"<TimesheetTask(Id={self.Id}, TimesheetId={self.TimesheetId}, "
            f"TaskItemId={self.TaskItemId}, TaskCodeId={self.TaskCodeId})>"
        )
