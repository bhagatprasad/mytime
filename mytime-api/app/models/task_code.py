from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# IMPORTANT
from app.models.task_Item import TaskItem


class TaskCode(Base):
    __tablename__ = "TaskCode"

    TaskCodeId = Column(BigInteger, primary_key=True, index=True)

    TaskItemId = Column(BigInteger, ForeignKey("TaskItem.TaskItemId"))
    Name = Column(Text, nullable=False)

    Code = Column(Text, nullable=False)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True)
    # ProjectId = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, default=True)

    task_item = relationship("TaskItem", back_populates="task_codes")
