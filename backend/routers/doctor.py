from fastapi import APIRouter, UploadFile, File, Form, Depends, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
import os
import tempfile

from database.connection import get_db
from services.doctor_service import DoctorService

router = APIRouter()


def _require_doctor_access(doctor_id: int, x_user_role: str, x_user_id: str) -> int:
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Missing authentication headers")
    if x_user_role.lower() != "doctor":
        raise HTTPException(status_code=403, detail="Doctor access required")
    try:
        header_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id header")
    if header_id != doctor_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return header_id


def _require_doctor_header(x_user_role: str, x_user_id: str) -> int:
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Missing authentication headers")
    if x_user_role.lower() != "doctor":
        raise HTTPException(status_code=403, detail="Doctor access required")
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id header")


class ScribeRequest(BaseModel):
    transcript: str
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None


class AppointmentStatusUpdate(BaseModel):
    status: str


@router.get("/dashboard")
def get_doctor_dashboard(
    doctor_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """Get doctor dashboard with statistics"""
    _require_doctor_access(doctor_id, x_user_role, x_user_id)
    return DoctorService.get_doctor_dashboard(db, doctor_id)


@router.get("/patients")
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """Get comprehensive patient list for a doctor"""
    _require_doctor_access(doctor_id, x_user_role, x_user_id)
    return DoctorService.get_doctor_patients(db, doctor_id)


@router.get("/patient")
def get_all_patients(db: Session = Depends(get_db)):
    """Compatibility endpoint that returns all patients in the system"""
    return DoctorService.get_all_patients(db)


@router.post("/scribe")
def post_doctor_scribe(payload: ScribeRequest):
    """Process text transcript and generate medical documents"""
    patient_info = None
    if payload.patient_name:
        patient_info = {
            "name": payload.patient_name,
            "age": payload.patient_age
        }
    return DoctorService.post_doctor_scribe(payload.transcript, patient_info)


@router.post("/scribe/audio")
async def post_doctor_scribe_audio(
    audio: UploadFile = File(...),
    patient_name: Optional[str] = Form(None),
    patient_age: Optional[int] = Form(None)
):
    """
    Upload audio file for transcription and medical document generation
    
    Accepts: WAV, MP3, FLAC, OGG audio files
    """
    # Validate file type
    allowed_types = ["audio/wav", "audio/mpeg", "audio/mp3", "audio/flac", "audio/ogg"]
    if audio.content_type not in allowed_types:
        return {
            "error": "Invalid file type",
            "message": f"Please upload audio file. Allowed types: {', '.join(allowed_types)}"
        }
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process audio file
        patient_info = None
        if patient_name:
            patient_info = {
                "name": patient_name,
                "age": patient_age
            }
        
        result = DoctorService.process_audio_transcription(temp_file_path, patient_info)
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        return result
    
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        return {
            "error": str(e),
            "message": "Error processing audio file"
        }


@router.post("/appointment/{appointment_id}/toggle-completion")
def toggle_appointment_completion(
    appointment_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Toggle appointment completion status
    
    Changes status from Completed to Scheduled or vice versa
    """
    doctor_id = _require_doctor_header(x_user_role, x_user_id)
    return DoctorService.toggle_appointment_completion(db, appointment_id, doctor_id)


@router.put("/appointment/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Update appointment status
    
    Valid statuses: Scheduled, In Progress, Completed, Cancelled
    """
    doctor_id = _require_doctor_header(x_user_role, x_user_id)
    return DoctorService.update_appointment_status(db, appointment_id, payload.status, doctor_id)


@router.get("/appointments-by-status")
def get_doctor_appointments_by_status(
    doctor_id: int,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Get doctor's appointments categorized by computed status (Active/Completed)
    
    Active: Appointments scheduled for today that are not manually completed
    Completed: Past appointments or manually completed appointments
    """
    _require_doctor_access(doctor_id, x_user_role, x_user_id)
    return DoctorService.get_doctor_appointments_with_status(db, doctor_id)


@router.get("/appointments-range")
def get_doctor_appointments_range(
    doctor_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None)
):
    """
    Get doctor's appointments between start and end dates (inclusive)
    """
    _require_doctor_access(doctor_id, x_user_role, x_user_id)
    return DoctorService.get_doctor_appointments_range(db, doctor_id, start_date, end_date)


# Made with Bob
