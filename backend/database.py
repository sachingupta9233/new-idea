"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import get_settings
import os

settings = get_settings()

# Get database URL (for Render deployment, use SQLite)
db_url = settings.DATABASE_URL

# Configure engine based on database type
if 'sqlite' in db_url:
    # SQLite configuration (for free tier / local development)
    engine = create_engine(
        db_url,
        echo=settings.SQLALCHEMY_ECHO,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration (for production)
    engine = create_engine(
        db_url,
        echo=settings.SQLALCHEMY_ECHO,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
