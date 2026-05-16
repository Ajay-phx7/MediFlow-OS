"""
Appointment model for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
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

    def get_computed_status(self):
        """
        Compute appointment status based on date and current status.
        Returns 'Active' for today's and future appointments that are not manually
        completed or cancelled. Past appointments display as 'Completed'.
        """
        if not self.scheduled_time:
            return self.status
        
        today = date.today()
        appointment_date = self.scheduled_time.date()
        
        # Show Active for today and future dates (if not manually completed/cancelled)
        if appointment_date >= today and self.status not in ["Completed", "Cancelled"]:
            return "Active"
        
        # Past dates or manually completed appointments show as Completed
        return "Completed"

    def to_dict(self, include_computed_status=False):
        """
        Convert model to dictionary
        
        Args:
            include_computed_status: If True, includes computed_status field
        """
        result = {
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
        
        if include_computed_status:
            result["computed_status"] = self.get_computed_status()
        
        return result

# Made with Bob
