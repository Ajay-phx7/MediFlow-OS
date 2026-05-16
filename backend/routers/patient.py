from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from database.connection import get_db
from services.patient_service import PatientService

router = APIRouter()


def _require_patient_access(patient_id: int, x_user_role: str, x_user_id: str) -> int:
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Missing authentication headers")
    if x_user_role.lower() != "patient":
        raise HTTPException(status_code=403, detail="Patient access required")
    try:
        header_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id header")
    if header_id != patient_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return header_id


class BookAppointmentRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str  # YYYY-MM-DD
    appointment_time: str  # HH:MM
    complaint: Optional[str] = None


@router.get("/dashboard")
def get_patient_dashboard(
    patient_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """Get comprehensive patient dashboard with appointments, prescriptions, and consultations"""
    _require_patient_access(patient_id, x_user_role, x_user_id)
    return PatientService.get_patient_dashboard(db, patient_id)


@router.get("/health-report")
def get_health_report(
    patient_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """Get detailed patient health report"""
    _require_patient_access(patient_id, x_user_role, x_user_id)
    return PatientService.get_health_report(db, patient_id)


@router.get("/doctors")
def get_available_doctors(db: Session = Depends(get_db)):
    """Get list of all available doctors for appointment booking"""
    return PatientService.get_available_doctors(db)


@router.get("/available-slots")
def get_available_slots(
    doctor_id: int,
    appointment_date: str,
    db: Session = Depends(get_db)
):
    """
    Get available time slots for a doctor on a specific date
    
    Args:
        doctor_id: ID of the doctor
        appointment_date: Date in YYYY-MM-DD format
    """
    return PatientService.get_available_slots(db, doctor_id, appointment_date)


@router.post("/book-appointment")
def book_appointment(
    payload: BookAppointmentRequest,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Book an appointment for a patient
    
    Request body:
        - patient_id: ID of the patient
        - doctor_id: ID of the doctor
        - appointment_date: Date in YYYY-MM-DD format
        - appointment_time: Time in HH:MM format
        - complaint: Optional complaint/reason for visit
    """
    _require_patient_access(payload.patient_id, x_user_role, x_user_id)
    return PatientService.book_appointment(
        db=db,
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
        complaint=payload.complaint
    )


@router.get("/appointments")
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Get all appointments for a patient
    
    Returns upcoming and past appointments with computed status
    """
    _require_patient_access(patient_id, x_user_role, x_user_id)
    return PatientService.get_patient_appointments(db, patient_id)


# Made with Bob
