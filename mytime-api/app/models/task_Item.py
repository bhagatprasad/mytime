from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from app.core.database import Base

class TaskItem(Base):
    __tablename__ = "TaskItem"

    TaskItemId = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Name = Column(Text, nullable=True)
    Code = Column(Text, nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
<<<<<<< HEAD
    ModifiedOn = Column(DateTime,   nullable=True)

    IsActive = Column(Boolean, default=True)
    ProjectId = Column(BigInteger, nullable=True)  
=======
    ModifiedOn = Column(DateTime(timezone=True), nullable=True)
    IsActive = Column(Boolean, nullable=True)
    ProjectId = Column(BigInteger, nullable=True)
>>>>>>> origin/main

    def __repr__(self):
        return f"<TaskItem(TaskItemId={self.TaskItemId}, Name='{self.Name}', Code='{self.Code}')>"