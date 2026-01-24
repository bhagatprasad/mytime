from sqlalchemy import create_engine, text  # ← ADDED 'text' here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with connection pooling
engine = None
SessionLocal = None

if settings.DATABASE_URL:
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            echo=settings.DATABASE_ECHO_SQL,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("✅ Database engine created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database engine: {e}")
        engine = None
        SessionLocal = None
else:
    logger.warning("⚠️  DATABASE_URL not set, database operations disabled")

Base = declarative_base()

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        raise Exception("Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection() -> bool:
    """Test database connection"""
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # ← FIXED: Added text() wrapper
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
