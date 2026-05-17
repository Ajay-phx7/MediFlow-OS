from datetime import date
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import get_db
from database.models import AdminUser
from services.admin_service import AdminService

router = APIRouter()


def _require_admin_access(
    db: Session,
    x_user_role: str,
    x_user_id: str,
    require_pharmacy: bool = False,
) -> AdminUser:
    if not x_user_role or not x_user_id:
        raise HTTPException(status_code=401, detail="Missing authentication headers")
    if x_user_role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        admin_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user id header")

    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin account not found")

    if require_pharmacy and admin.department != "Pharmacy":
        raise HTTPException(status_code=403, detail="Pharmacy access required")

    return admin


class CreatePatientRequest(BaseModel):
    name: str
    date_of_birth: date
    age: int
    blood_group: str | None = None
    allergies: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class CreateDoctorRequest(BaseModel):
    name: str
    department_id: int
    specialization: str | None = None
    is_available: bool = True


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    return AdminService.get_admin_stats(db)


@router.get("/queue")
def get_queue(db: Session = Depends(get_db)):
    return AdminService.get_queue(db)


@router.get("/surge-forecast")
def get_surge_forecast():
    return AdminService.get_surge_forecast()


@router.get("/live-map")
def get_live_map(db: Session = Depends(get_db)):
    return AdminService.get_live_map(db)


@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None),
):
    _require_admin_access(db, x_user_role, x_user_id)
    return AdminService.get_departments(db)


@router.post("/patients")
def create_patient(
    payload: CreatePatientRequest,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None),
):
    _require_admin_access(db, x_user_role, x_user_id)
    return AdminService.create_patient(db, payload.model_dump())


@router.post("/doctors")
def create_doctor(
    payload: CreateDoctorRequest,
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None),
):
    _require_admin_access(db, x_user_role, x_user_id)
    return AdminService.create_doctor(db, payload.model_dump())


@router.get("/medicine-inventory")
def get_medicine_inventory(
    db: Session = Depends(get_db),
    x_user_role: str = Header(None),
    x_user_id: str = Header(None),
):
    _require_admin_access(db, x_user_role, x_user_id, require_pharmacy=True)
    return AdminService.get_medicine_inventory()


class SendChatMessageRequest(BaseModel):
    department: str
    sender_username: str
    message_text: str


@router.get("/chat/all")
def get_all_chat(db: Session = Depends(get_db)):
    """Get all chat messages across all departments"""
    return AdminService.get_all_chat_messages(db)


@router.get("/chat/{department}")
def get_department_chat(department: str, db: Session = Depends(get_db)):
    """Get chat messages for a specific department"""
    return AdminService.get_chat_messages(db, department)


@router.post("/chat")
def send_chat_message(request: SendChatMessageRequest, db: Session = Depends(get_db)):
    """Send a new chat message to a department"""
    return AdminService.send_chat_message(
        db, 
        request.department, 
        request.sender_username, 
        request.message_text
    )

