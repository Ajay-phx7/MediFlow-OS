"""
Appointment model for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Appointment(Base):
    """
    Appointment model representing scheduled doctor-patient appointments
    """
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    scheduled_time = Column(DateTime, nullable=False, index=True)
    status = Column(String, default="Scheduled")  # Scheduled, In Progress, Completed, Cancelled
    complaint = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    consultation = relationship("Consultation", back_populates="appointment", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Appointment(id={self.id}, patient='{self.patient.name if self.patient else None}', doctor='{self.doctor.name if self.doctor else None}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_name": self.patient.name if self.patient else None,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor.name if self.doctor else None,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status,
            "complaint": self.complaint,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
