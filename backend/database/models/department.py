"""
Department model for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Department(Base):
    """
    Department model representing hospital departments
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    current_patients = Column(Integer, default=0)
    congestion_level = Column(String, default="Low")  # Low, Moderate, High
    estimated_wait_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    doctors = relationship("Doctor", back_populates="department", cascade="all, delete-orphan")
    queue_entries = relationship("QueueEntry", back_populates="department", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', patients={self.current_patients})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "patients": self.current_patients,
            "congestion": self.congestion_level,
            "er_wait_min": self.estimated_wait_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
