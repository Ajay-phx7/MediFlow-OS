from fastapi import APIRouter
from pydantic import BaseModel

from mock_data.doctors import DOCTOR_DASHBOARD, DOCTOR_PATIENTS, SCRIBE_RESPONSE

router = APIRouter()


class ScribeRequest(BaseModel):
    transcript: str


@router.get("/dashboard")
def get_doctor_dashboard():
    return DOCTOR_DASHBOARD


@router.get("/patients")
def get_doctor_patients():
    return {"patients": DOCTOR_PATIENTS}


@router.post("/scribe")
def post_doctor_scribe(payload: ScribeRequest):
    return {
        "notes": SCRIBE_RESPONSE["notes"],
        "prescription": SCRIBE_RESPONSE["prescription"],
        "received_transcript": payload.transcript,
    }
