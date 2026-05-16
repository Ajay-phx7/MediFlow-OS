"""
Prescription models for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Prescription(Base):
    """
    Prescription model representing medication prescriptions
    """
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), unique=True, index=True)
    prescribed_date = Column(DateTime, default=datetime.utcnow, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    consultation = relationship("Consultation", back_populates="prescription")
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Prescription(id={self.id}, patient='{self.patient.name if self.patient else None}', doctor='{self.doctor.name if self.doctor else None}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_name": self.patient.name if self.patient else None,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor.name if self.doctor else None,
            "consultation_id": self.consultation_id,
            "prescribed_date": self.prescribed_date.isoformat() if self.prescribed_date else None,
            "notes": self.notes,
            "medications": [item.to_dict() for item in self.items] if self.items else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PrescriptionItem(Base):
    """
    PrescriptionItem model representing individual medications in a prescription
    """
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False, index=True)
    medication_name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    duration = Column(String)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    prescription = relationship("Prescription", back_populates="items")

    def __repr__(self):
        return f"<PrescriptionItem(id={self.id}, medication='{self.medication_name}', dosage='{self.dosage}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "medication": self.medication_name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "duration": self.duration,
            "instructions": self.instructions,
        }

# Made with Bob
