from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.admin_service import AdminService

router = APIRouter()


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


from pydantic import BaseModel


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

