"""
CRUD operations for Appointment model
"""

from typing import List, Optional
from datetime import datetime, date, timedelta
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

    def get_by_doctor_between(self, db: Session, doctor_id: int, start_date: date, end_date: date) -> List[Appointment]:
        """Get appointments for a doctor between start and end dates (inclusive)."""
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date + timedelta(days=1), datetime.min.time())
        return db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time >= start_dt,
            Appointment.scheduled_time < end_dt
        ).order_by(Appointment.scheduled_time).all()
    
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
    
    def get_active_for_doctor(self, db: Session, doctor_id: int) -> List[Appointment]:
        """Get active appointments for a doctor (today's appointments that are not completed)"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        return db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time >= today,
            Appointment.scheduled_time < tomorrow,
            Appointment.status.in_(["Scheduled", "In Progress", "Active"])
        ).order_by(Appointment.scheduled_time).all()
    
    def get_completed_for_doctor(self, db: Session, doctor_id: int) -> List[Appointment]:
        """Get completed appointments for a doctor"""
        return db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "Completed"
        ).order_by(Appointment.scheduled_time.desc()).all()
    
    def create_appointment(
        self,
        db: Session,
        patient_id: int,
        doctor_id: int,
        scheduled_time: datetime,
        complaint: Optional[str] = None
    ) -> Appointment:
        """Create a new appointment"""
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            scheduled_time=scheduled_time,
            status="Scheduled",
            complaint=complaint,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment
    
    def update_status(self, db: Session, appointment_id: int, status: str) -> Appointment:
        """Update appointment status"""
        appointment = self.get(db, appointment_id)
        if appointment:
            appointment.status = status
            appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
        return appointment
    
    def toggle_completion(self, db: Session, appointment_id: int) -> Appointment:
        """Toggle appointment between Completed and Scheduled/In Progress status"""
        appointment = self.get(db, appointment_id)
        if appointment:
            if appointment.status == "Completed":
                # If completed, change back to Scheduled
                appointment.status = "Scheduled"
            else:
                # If not completed (Scheduled, In Progress, etc.), mark as Completed
                appointment.status = "Completed"
            appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
        return appointment
    
    def get_available_slots(
        self,
        db: Session,
        doctor_id: int,
        target_date: date,
        exclude_appointment_id: Optional[int] = None,
    ) -> List[str]:
        """
        Get available time slots for a doctor on a specific date
        Returns list of available time slots in HH:MM format
        """
        # Define working hours (9 AM to 5 PM, 30-minute slots)
        start_hour = 9
        end_hour = 17
        slot_duration = 30  # minutes

        start_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=start_hour)
        end_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=end_hour)

        # Get existing appointments for the doctor on that date
        existing_appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_time >= start_dt,
            Appointment.scheduled_time < end_dt,
            Appointment.status != "Cancelled"
        ).all()

        if exclude_appointment_id is not None:
            existing_appointments = [
                appt for appt in existing_appointments if appt.id != exclude_appointment_id
            ]
        
        # Create set of booked times
        booked_times = {appt.scheduled_time.strftime("%H:%M") for appt in existing_appointments}
        
        # Generate all possible slots
        available_slots = []
        current_time = start_dt
        end_time = end_dt
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            if time_str not in booked_times:
                available_slots.append(time_str)
            current_time += timedelta(minutes=slot_duration)
        
        return available_slots

    def cancel_appointment(self, db: Session, appointment_id: int) -> Optional[Appointment]:
        """Cancel an appointment without deleting it"""
        appointment = self.get(db, appointment_id)
        if appointment:
            appointment.status = "Cancelled"
            appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
        return appointment

    def reschedule_appointment(
        self,
        db: Session,
        appointment_id: int,
        scheduled_time: datetime,
    ) -> Optional[Appointment]:
        """Move an appointment to a new future time"""
        appointment = self.get(db, appointment_id)
        if appointment:
            appointment.scheduled_time = scheduled_time
            appointment.status = "Scheduled"
            appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(appointment)
        return appointment


# Create instance
appointment = CRUDAppointment(Appointment)

# Made with Bob
