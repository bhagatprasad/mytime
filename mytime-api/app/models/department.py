from sqlalchemy import Boolean, Column, DateTime, Text, BigInteger, func
from app.core.database import Base


class Department(Base):
    __tablename__ = "Department"

    DepartmentId = Column(BigInteger, primary_key=True, index=True)

    Name = Column(Text, nullable=True)
    Description = Column(Text, nullable=True)

    Code = Column(Text, nullable=True)

    # Common fields (from Common base class)
    CreatedOn = Column(DateTime,   nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<Department("
            f"DepartmentId={self.DepartmentId}, "
            f"Name='{self.Name}', "
            f"Code='{self.Code}')>"
        )
