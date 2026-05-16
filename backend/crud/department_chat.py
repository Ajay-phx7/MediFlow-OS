"""
CRUD operations for DepartmentChatMessage model
"""

from sqlalchemy.orm import Session
from database.models import DepartmentChatMessage


def create_message(db: Session, department: str, sender_username: str, message_text: str) -> DepartmentChatMessage:
    """Create a new chat message"""
    message = DepartmentChatMessage(
        department=department,
        sender_username=sender_username,
        message_text=message_text
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_by_department(db: Session, department: str, limit: int = 100):
    """Get chat messages for a specific department, ordered by timestamp (newest first)"""
    return (
        db.query(DepartmentChatMessage)
        .filter(DepartmentChatMessage.department == department)
        .order_by(DepartmentChatMessage.timestamp.desc())
        .limit(limit)
        .all()
    )


def get_all(db: Session, limit: int = 100):
    """Get all chat messages across all departments, ordered by timestamp (newest first)"""
    return (
        db.query(DepartmentChatMessage)
        .order_by(DepartmentChatMessage.timestamp.desc())
        .limit(limit)
        .all()
    )


# Made with Bob