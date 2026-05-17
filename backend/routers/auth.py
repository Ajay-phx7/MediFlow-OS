"""
Authentication router for MediFlow OS
Provides simple selection-based login for doctors and patients (no password required)
"""

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database.connection import get_db
from database.models import Doctor, Patient, AdminUser
from services.patient_service import PatientService

router = APIRouter()


class AdminLoginResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    username: str
    department: str


class DoctorLoginResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    name: str
    department: str
    specialization: Optional[str]


class PatientLoginResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    name: str
    age: Optional[int]
    blood_group: Optional[str]


class PatientSignupRequest(BaseModel):
    name: str
    date_of_birth: date
    age: int
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


@router.get("/doctors", response_model=List[DoctorLoginResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    """
    Get list of all doctors for selection-based login
    No password authentication required
    """
    doctors = db.query(Doctor).all()
    
    return [
        DoctorLoginResponse.model_validate({
            "id": doctor.id,
            "name": doctor.name,
            "department": doctor.department.name if doctor.department else "Unknown",
            "specialization": doctor.specialization
        })
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
        PatientLoginResponse.model_validate(patient)
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
            "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth is not None else None,
            "blood_group": patient.blood_group,
            "allergies": patient.allergies,
            "phone": patient.phone,
            "email": patient.email
        },
        "message": f"Logged in as {patient.name}"
    }


@router.post("/patients/signup")
def signup_patient(payload: PatientSignupRequest, db: Session = Depends(get_db)):
    """Public patient signup endpoint"""
    return PatientService.signup_patient(db, payload.model_dump())


# Made with Bob


@router.get("/admins", response_model=List[AdminLoginResponse])
def get_all_admins(db: Session = Depends(get_db)):
    """
    Get list of all admin accounts for selection-based login
    No password authentication required
    """
    admins = db.query(AdminUser).all()
    
    return [
        AdminLoginResponse.model_validate(admin)
        for admin in admins
    ]


@router.get("/admins/{admin_id}")
def login_as_admin(admin_id: int, db: Session = Depends(get_db)):
    """
    Login as a specific admin by selecting their ID
    Returns admin information and access token
    """
    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin account not found")
    
    return {
        "success": True,
        "admin": {
            "id": admin.id,
            "username": admin.username,
            "department": admin.department,
            "created_at": admin.created_at.isoformat()
        },
        "message": f"Logged in as {admin.username}"
    }

