"""
Authentication router for MediFlow OS
Provides simple selection-based login for doctors and patients (no password required)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database.connection import get_db
from database.models import Doctor, Patient

router = APIRouter()


class DoctorLoginResponse(BaseModel):
    id: int
    name: str
    department: str
    specialization: Optional[str]


class PatientLoginResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]
    blood_group: Optional[str]


@router.get("/doctors", response_model=List[DoctorLoginResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    """
    Get list of all doctors for selection-based login
    No password authentication required
    """
    doctors = db.query(Doctor).all()
    
    return [
        DoctorLoginResponse(
            id=doctor.id,
            name=doctor.name,
            department=doctor.department.name if doctor.department else "Unknown",
            specialization=doctor.specialization
        )
        for doctor in doctors
    ]


@router.get("/doctors/{doctor_id}")
def login_as_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Login as a specific doctor by selecting their ID
    Returns doctor information and access token
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return {
        "success": True,
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "department": doctor.department.name if doctor.department else "Unknown",
            "department_id": doctor.department_id,
            "specialization": doctor.specialization,
            "is_available": doctor.is_available,
            "appointments_today": doctor.appointments_today
        },
        "message": f"Logged in as {doctor.name}"
    }


@router.get("/patients", response_model=List[PatientLoginResponse])
def get_all_patients(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of all patients for selection-based login
    Supports search by name
    No password authentication required
    """
    query = db.query(Patient)
    
    if search:
        query = query.filter(Patient.name.ilike(f"%{search}%"))
    
    patients = query.all()
    
    return [
        PatientLoginResponse(
            id=patient.id,
            name=patient.name,
            age=patient.age,
            blood_group=patient.blood_group
        )
        for patient in patients
    ]


@router.get("/patients/{patient_id}")
def login_as_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Login as a specific patient by selecting their ID
    Returns patient information and access token
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "success": True,
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            "blood_group": patient.blood_group,
            "allergies": patient.allergies,
            "phone": patient.phone,
            "email": patient.email
        },
        "message": f"Logged in as {patient.name}"
    }


# Made with Bob