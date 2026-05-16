"""
CRUD operations for Queue model
"""

from typing import List
from sqlalchemy.orm import Session
from database.models.queue import QueueEntry
from crud.base import CRUDBase


class CRUDQueue(CRUDBase[QueueEntry]):
    """CRUD operations for Queue"""
    
    def get_by_department(self, db: Session, department_id: int) -> List[QueueEntry]:
        """Get all queue entries for a department"""
        return db.query(QueueEntry).filter(
            QueueEntry.department_id == department_id
        ).order_by(QueueEntry.priority.desc(), QueueEntry.joined_at).all()
    
    def get_waiting(self, db: Session) -> List[QueueEntry]:
        """Get all waiting queue entries"""
        return db.query(QueueEntry).filter(
            QueueEntry.status == "Waiting"
        ).order_by(QueueEntry.priority.desc(), QueueEntry.joined_at).all()
    
    def get_by_token(self, db: Session, token: str) -> QueueEntry:
        """Get queue entry by token number"""
        return db.query(QueueEntry).filter(QueueEntry.token_number == token).first()
    
    def get_by_patient(self, db: Session, patient_id: int) -> List[QueueEntry]:
        """Get queue entries for a patient"""
        return db.query(QueueEntry).filter(QueueEntry.patient_id == patient_id).all()


# Create instance
queue = CRUDQueue(QueueEntry)

# Made with Bob
