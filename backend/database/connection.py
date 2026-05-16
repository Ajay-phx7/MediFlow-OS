"""
Database connection and session management for MediFlow OS
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Database configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/mediflow.db"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging during development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    Usage in FastAPI endpoints:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables
    Should be called once during application startup
    """
    # Import all models here to ensure they are registered with Base
    from database.models import (
        department, doctor, patient, appointment,
        queue, consultation, prescription, medical_record,
        admin_user, department_chat
    )
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_all_tables():
    """
    Drop all tables - USE WITH CAUTION!
    Only for development/testing purposes
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped!")

# Made with Bob
