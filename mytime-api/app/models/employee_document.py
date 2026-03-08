from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text
from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from app.core.database import Base


class EmployeeDocument(Base):
    __tablename__ = "EmployeeDocuments"

    EmployeeDocumentId = Column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    EmployeeId = Column(BigInteger, nullable=True)
    DocumentType = Column(String(255), nullable=True)
    FileId = Column(String(255), nullable=True)
    FileName = Column(String(500), nullable=True)
    BucketId = Column(String(255), nullable=True)
    ContentLength = Column(BigInteger, nullable=True)
    ContentType = Column(String(255), nullable=True)
    FileInfo = Column(Text, nullable=True)
    UploadTimestamp = Column(DateTime, nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"<EmployeeDocument(EmployeeDocumentId={self.EmployeeDocumentId}, FileName='{self.FileName}')>"
