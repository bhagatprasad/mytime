from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# For SQL Server, we need to handle special characters in password
# Password contains @ which needs to be URL encoded
def create_db_engine():
    """Create SQLAlchemy engine with proper configuration for SQL Server"""
    try:
        # Create engine with SQL Server specific parameters
        engine = create_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,   # Recycle connections every hour
            echo=settings.DATABASE_ECHO_SQL,
            connect_args={
                "timeout": 30,
                "login_timeout": 30,
            }
        )
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise

# Create engine
engine = create_db_engine()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection using text() for SQL expression"""
    try:
        with engine.connect() as conn:
            # Use text() for raw SQL queries
            result = conn.execute(text("SELECT 1 AS test"))
            return result.fetchone() is not None
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False