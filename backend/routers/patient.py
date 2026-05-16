from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.patient_service import PatientService

router = APIRouter()


@router.get("/dashboard")
def get_patient_dashboard(patient_id: int = None, db: Session = Depends(get_db)):
    """Get comprehensive patient dashboard with appointments, prescriptions, and consultations"""
    return PatientService.get_patient_dashboard(db, patient_id)


@router.get("/health-report")
def get_health_report(patient_id: int = None, db: Session = Depends(get_db)):
    """Get detailed patient health report"""
    return PatientService.get_health_report(db, patient_id)

# Made with Bob
