"""
Doctor model for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Doctor(Base):
    """
    Doctor model representing medical practitioners
    """
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    specialization = Column(String)
    is_available = Column(Boolean, default=True)
    appointments_today = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="doctor", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor(id={self.id}, name='{self.name}', department='{self.department.name if self.department else None}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department.name if self.department else None,
            "department_id": self.department_id,
            "specialization": self.specialization,
            "is_available": self.is_available,
            "appointments_today": self.appointments_today,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
