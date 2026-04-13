# # from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Numeric
# # from sqlalchemy.orm import relationship
# # from sqlalchemy.sql import func
# # from app.core.database import Base


# # class TimesheetTask(Base):
# #     __tablename__ = "TimesheetTask"

# #     Id = Column(BigInteger, primary_key=True, index=True)

# #     TimesheetId = Column(BigInteger, ForeignKey("Timesheet.Id"), nullable=True)
# #     TaskItemId = Column(BigInteger, ForeignKey("TaskItem.TaskItemId"), nullable=True)
# #     TaskCodeId = Column(BigInteger, ForeignKey("TaskCode.TaskCodeId"), nullable=True)

# #     MondayHours = Column(BigInteger, nullable=True)
# #     TuesdayHours = Column(BigInteger, nullable=True)
# #     WednesdayHours = Column(BigInteger, nullable=True)
# #     ThursdayHours = Column(BigInteger, nullable=True)
# #     FridayHours = Column(BigInteger, nullable=True)
# #     SaturdayHours = Column(BigInteger, nullable=True)
# #     SundayHours = Column(BigInteger, nullable=True)

# #     CreatedBy = Column(BigInteger, nullable=True)
# #     CreatedOn = Column(DateTime,   nullable=True)
# #     ModifiedBy = Column(BigInteger, nullable=True)
# #     ModifiedOn = Column(DateTime,   nullable=True)

# #     IsActive = Column(Boolean, nullable=True)
# #     TotalHrs = Column(Numeric(18, 0), nullable=True)
# #     # Relationships
# #     timesheet = relationship("Timesheet", back_populates="timesheet_tasks")
# #     task_item = relationship("TaskItem")
# #     task_code = relationship("TaskCode")

# #     def __repr__(self):
# #         return (
# #             f"<TimesheetTask(Id={self.Id}, TimesheetId={self.TimesheetId}, "
# #             f"TaskItemId={self.TaskItemId}, TaskCodeId={self.TaskCodeId})>"
# #         )

# from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Numeric
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.core.database import Base


# class TimesheetTask(Base):
#     __tablename__ = "TimesheetTask"

#     Id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

#     TimesheetId = Column(BigInteger, ForeignKey("Timesheet.Id"), nullable=True)
#     TaskItemId = Column(BigInteger, ForeignKey("TaskItem.TaskItemId"), nullable=True)
#     TaskCodeId = Column(BigInteger, ForeignKey("TaskCode.TaskCodeId"), nullable=True)

#     MondayHours = Column(BigInteger, nullable=True)
#     TuesdayHours = Column(BigInteger, nullable=True)
#     WednesdayHours = Column(BigInteger, nullable=True)
#     ThursdayHours = Column(BigInteger, nullable=True)
#     FridayHours = Column(BigInteger, nullable=True)
#     SaturdayHours = Column(BigInteger, nullable=True)
#     SundayHours = Column(BigInteger, nullable=True)

#     CreatedBy = Column(BigInteger, nullable=True)

#     # ✅ FIX START
#     CreatedOn = Column(DateTime(timezone=True), default=func.now())
#     ModifiedBy = Column(BigInteger, nullable=True)
#     ModifiedOn = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
#     # ✅ FIX END

#     IsActive = Column(Boolean, nullable=True)
#     TotalHrs = Column(Numeric(18, 0), nullable=True)

#     # Relationships
#     timesheet = relationship("Timesheet", back_populates="timesheet_tasks")
#     task_item = relationship("TaskItem")
#     task_code = relationship("TaskCode")

#     def __repr__(self):
#         return (
#             f"<TimesheetTask(Id={self.Id}, TimesheetId={self.TimesheetId}, "
#             f"TaskItemId={self.TaskItemId}, TaskCodeId={self.TaskCodeId})>"
#         )

from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class TimesheetTask(Base):
    __tablename__ = "TimesheetTask"

    Id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    TimesheetId = Column(BigInteger, ForeignKey("Timesheet.Id"), nullable=True)
    TaskItemId = Column(BigInteger, nullable=True)
    TaskCodeId = Column(BigInteger, nullable=True)
    MondayHours = Column(BigInteger, nullable=True)
    TuesdayHours = Column(BigInteger, nullable=True)
    WednesdayHours = Column(BigInteger, nullable=True)
    ThursdayHours = Column(BigInteger, nullable=True)
    FridayHours = Column(BigInteger, nullable=True)
    SaturdayHours = Column(BigInteger, nullable=True)
    SundayHours = Column(BigInteger, nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True)
    IsActive = Column(Boolean, nullable=True)
    TotalHrs = Column(Numeric(18, 0), nullable=True)

    # Relationship back to Timesheet
    timesheet = relationship("Timesheet", back_populates="timesheet_tasks")

    def __repr__(self):
        return f"<TimesheetTask(Id={self.Id}, TimesheetId={self.TimesheetId})>"