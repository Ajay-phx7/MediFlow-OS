"""
Consultation model for MediFlow OS
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Consultation(Base):
    """
    Consultation model representing doctor-patient consultations
    """
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    soap_notes = Column(Text)  # SOAP format notes
    transcript = Column(Text)  # Raw consultation transcript
    consultation_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointment = relationship("Appointment", back_populates="consultation")
    doctor = relationship("Doctor", back_populates="consultations")
    patient = relationship("Patient", back_populates="consultations")
    prescription = relationship("Prescription", back_populates="consultation", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Consultation(id={self.id}, patient='{self.patient.name if self.patient else None}', doctor='{self.doctor.name if self.doctor else None}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor.name if self.doctor else None,
            "patient_id": self.patient_id,
            "patient_name": self.patient.name if self.patient else None,
            "soap_notes": self.soap_notes,
            "transcript": self.transcript,
            "consultation_date": self.consultation_date.isoformat() if self.consultation_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
