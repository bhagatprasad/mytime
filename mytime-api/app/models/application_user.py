from sqlalchemy import Column, BigInteger, Text
from app.core.database import Base


class ApplicationUser(Base):
    __tablename__ = "ApplicationUser"

    Id = Column(BigInteger, primary_key=True, index=True)

    FirstName = Column(Text, nullable=True)
    LastName = Column(Text, nullable=True)
    Email = Column(Text, nullable=True)
    Phone = Column(Text, nullable=True)

    DepartmentId = Column(BigInteger, nullable=True)
    RoleId = Column(BigInteger, nullable=True)

    def __repr__(self):
        return (
            f"<ApplicationUser("
            f"Id={self.Id}, "
            f"Email='{self.Email}')>"
        )
