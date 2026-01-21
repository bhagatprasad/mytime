from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TaskCode(Base):
    __tablename__ = "TaskCode"

    TaskCodeId = Column(BigInteger, primary_key=True, index=True)
    Name = Column(Text, nullable=False)
    Code = Column(Text, nullable=False)

    TaskItemId = Column(BigInteger, ForeignKey("TaskItem.TaskItemId"), nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, default=True)

    # Relationship to TaskItem
    task_item = relationship("TaskItem", backref="task_codes")

    def __repr__(self):
        return f"<TaskCode(TaskCodeId={self.TaskCodeId}, Name='{self.Name}', Code='{self.Code}')>"
