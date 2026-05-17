"""
CRUD operations for Doctor model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.doctor import Doctor
from crud.base import CRUDBase


class CRUDDoctor(CRUDBase[Doctor]):
    """CRUD operations for Doctor"""

    def create(
        self,
        db: Session,
        *,
        name: str,
        department_id: int,
        specialization: Optional[str] = None,
        is_available: bool = True,
        appointments_today: int = 0,
    ) -> Doctor:
        """Create a new doctor"""
        doctor = Doctor(
            name=name,
            department_id=department_id,
            specialization=specialization,
            is_available=is_available,
            appointments_today=appointments_today,
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        return doctor
    
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
