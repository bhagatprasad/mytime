from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TaskItem(Base):
    __tablename__ = "TaskItem"

    TaskItemId = Column(BigInteger, primary_key=True, index=True)
    Name = Column(Text, nullable=False)
    Code = Column(Text, nullable=False)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)

    IsActive = Column(Boolean, default=True)

    # One-to-many relationship to TaskCode
    task_codes = relationship("TaskCode", back_populates="task_item")

    def __repr__(self):
        return f"<TaskItem(TaskItemId={self.TaskItemId}, Name='{self.Name}', Code='{self.Code}')>"
