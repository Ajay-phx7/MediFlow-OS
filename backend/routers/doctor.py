from fastapi import APIRouter, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import os
import tempfile

from database.connection import get_db
from services.doctor_service import DoctorService

router = APIRouter()


class ScribeRequest(BaseModel):
    transcript: str
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None


@router.get("/dashboard")
def get_doctor_dashboard(doctor_id: int = None, db: Session = Depends(get_db)):
    """Get doctor dashboard with statistics"""
    return DoctorService.get_doctor_dashboard(db, doctor_id)


@router.get("/patients")
def get_doctor_patients(doctor_id: int = None, db: Session = Depends(get_db)):
    """Get comprehensive patient list for a doctor"""
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


# Made with Bob
