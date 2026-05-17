"""
CRUD operations for Patient model
"""

from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.patient import Patient
from crud.base import CRUDBase


class CRUDPatient(CRUDBase[Patient]):
    """CRUD operations for Patient"""

    def create(
        self,
        db: Session,
        *,
        name: str,
        date_of_birth: Optional[date] = None,
        age: Optional[int] = None,
        blood_group: Optional[str] = None,
        allergies: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Patient:
        """Create a new patient"""
        patient = Patient(
            name=name,
            date_of_birth=date_of_birth,
            age=age,
            blood_group=blood_group,
            allergies=allergies,
            phone=phone,
            email=email,
            address=address,
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    def get_by_name(self, db: Session, name: str) -> Optional[Patient]:
        """Get patient by name"""
        return db.query(Patient).filter(Patient.name == name).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Patient]:
        """Get patient by email"""
        return db.query(Patient).filter(Patient.email == email).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[Patient]:
        """Get patient by phone"""
        return db.query(Patient).filter(Patient.phone == phone).first()
    
    def search(self, db: Session, query: str) -> List[Patient]:
        """Search patients by name"""
        return db.query(Patient).filter(Patient.name.ilike(f"%{query}%")).all()


# Create instance
patient = CRUDPatient(Patient)

# Made with Bob
