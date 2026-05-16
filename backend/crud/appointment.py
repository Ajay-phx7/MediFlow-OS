"""
CRUD operations for Appointment model
"""

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from database.models.appointment import Appointment
from crud.base import CRUDBase


class CRUDAppointment(CRUDBase[Appointment]):
    """CRUD operations for Appointment"""
    
    def get_by_patient(self, db: Session, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).order_by(Appointment.scheduled_time.desc()).all()
    
    def get_by_doctor(self, db: Session, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a doctor"""
        return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).order_by(Appointment.scheduled_time).all()
    
    def get_today(self, db: Session, doctor_id: int) -> List[Appointment]:
        """Get today's appointments for a doctor"""
        today = datetime.now().date()
        return db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time >= today
        ).order_by(Appointment.scheduled_time).all()
    
    def get_by_status(self, db: Session, status: str) -> List[Appointment]:
        """Get appointments by status"""
        return db.query(Appointment).filter(Appointment.status == status).all()


# Create instance
appointment = CRUDAppointment(Appointment)

# Made with Bob
