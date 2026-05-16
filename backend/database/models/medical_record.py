"""
Medical record models for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class MedicalRecord(Base):
    """
    MedicalRecord model representing patient diagnoses and medical history
    """
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    diagnosis = Column(String, nullable=False)
    notes = Column(Text)
    diagnosis_date = Column(Date, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="medical_records")

    def __repr__(self):
        return f"<MedicalRecord(id={self.id}, patient='{self.patient.name if self.patient else None}', diagnosis='{self.diagnosis}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis,
            "notes": self.notes,
            "diagnosis_date": self.diagnosis_date.isoformat() if self.diagnosis_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Medication(Base):
    """
    Medication model representing current patient medications
    """
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    medication_name = Column(String, nullable=False)
    dosage = Column(String)
    is_active = Column(Boolean, default=True)
    started_date = Column(Date)
    ended_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="medications")

    def __repr__(self):
        return f"<Medication(id={self.id}, patient='{self.patient.name if self.patient else None}', medication='{self.medication_name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "is_active": self.is_active,
            "started_date": self.started_date.isoformat() if self.started_date else None,
            "ended_date": self.ended_date.isoformat() if self.ended_date else None,
        }


class LabResult(Base):
    """
    LabResult model representing laboratory test results
    """
    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    test_name = Column(String, nullable=False)
    value = Column(String)
    unit = Column(String)
    test_date = Column(Date, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="lab_results")

    def __repr__(self):
        return f"<LabResult(id={self.id}, patient='{self.patient.name if self.patient else None}', test='{self.test_name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "test": self.test_name,
            "value": self.value,
            "unit": self.unit,
            "date": self.test_date.isoformat() if self.test_date else None,
            "notes": self.notes,
        }


class Vaccination(Base):
    """
    Vaccination model representing patient vaccination records
    """
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    vaccine_name = Column(String, nullable=False)
    vaccination_date = Column(Date, index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="vaccinations")

    def __repr__(self):
        return f"<Vaccination(id={self.id}, patient='{self.patient.name if self.patient else None}', vaccine='{self.vaccine_name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "vaccine_name": self.vaccine_name,
            "vaccination_date": self.vaccination_date.isoformat() if self.vaccination_date else None,
            "notes": self.notes,
        }

# Made with Bob
