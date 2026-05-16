"""
CRUD operations for Patient model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.patient import Patient
from crud.base import CRUDBase


class CRUDPatient(CRUDBase[Patient]):
    """CRUD operations for Patient"""
    
    def get_by_name(self, db: Session, name: str) -> Optional[Patient]:
        """Get patient by name"""
        return db.query(Patient).filter(Patient.name == name).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Patient]:
        """Get patient by email"""
        return db.query(Patient).filter(Patient.email == email).first()
    
    def search(self, db: Session, query: str) -> List[Patient]:
        """Search patients by name"""
        return db.query(Patient).filter(Patient.name.ilike(f"%{query}%")).all()


# Create instance
patient = CRUDPatient(Patient)

# Made with Bob
