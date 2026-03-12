from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from app.core.database import Base

class TaskCode(Base):
    __tablename__ = "TaskCode"

    TaskCodeId = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Name = Column(Text, nullable=True)
    Code = Column(Text, nullable=True)
    TaskItemId = Column(BigInteger, nullable=True)  # Regular column, no ForeignKey
    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), nullable=True)
    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<TaskCode(TaskCodeId={self.TaskCodeId}, Name='{self.Name}', Code='{self.Code}')>"