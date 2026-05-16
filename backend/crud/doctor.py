"""
CRUD operations for Doctor model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.doctor import Doctor
from crud.base import CRUDBase


class CRUDDoctor(CRUDBase[Doctor]):
    """CRUD operations for Doctor"""
    
    def get_by_department(self, db: Session, department_id: int) -> List[Doctor]:
        """Get all doctors in a department"""
        return db.query(Doctor).filter(Doctor.department_id == department_id).all()
    
    def get_available(self, db: Session) -> List[Doctor]:
        """Get all available doctors"""
        return db.query(Doctor).filter(Doctor.is_available == True).all()
    
    def get_by_name(self, db: Session, name: str) -> Optional[Doctor]:
        """Get doctor by name"""
        return db.query(Doctor).filter(Doctor.name == name).first()


# Create instance
doctor = CRUDDoctor(Doctor)

# Made with Bob
