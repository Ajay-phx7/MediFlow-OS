from fastapi import APIRouter

from mock_data.patients import PATIENT_DASHBOARD, PATIENT_HEALTH_REPORT

router = APIRouter()


@router.get("/dashboard")
def get_patient_dashboard():
    return PATIENT_DASHBOARD


@router.get("/health-report")
def get_health_report():
    return PATIENT_HEALTH_REPORT
