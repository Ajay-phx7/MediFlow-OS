"""
Queue model for MediFlow OS
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class QueueEntry(Base):
    """
    QueueEntry model representing patients in queue
    """
    __tablename__ = "queue_entries"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    token_number = Column(String, unique=True, nullable=False, index=True)
    wait_time_minutes = Column(Integer, default=0)
    status = Column(String, default="Waiting")  # Waiting, In Consultation, Done, Cancelled
    priority = Column(Integer, default=0)  # Higher number = higher priority
    joined_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="queue_entries")
    department = relationship("Department", back_populates="queue_entries")

    def __repr__(self):
        return f"<QueueEntry(id={self.id}, token='{self.token_number}', patient='{self.patient.name if self.patient else None}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.patient.name if self.patient else None,
            "patient_id": self.patient_id,
            "token": self.token_number,
            "department": self.department.name if self.department else None,
            "department_id": self.department_id,
            "wait_time_min": self.wait_time_minutes,
            "status": self.status,
            "priority": self.priority,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
