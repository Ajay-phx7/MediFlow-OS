"""
CRUD operations for Department model
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models.department import Department
from crud.base import CRUDBase


class CRUDDepartment(CRUDBase[Department]):
    """CRUD operations for Department"""
    
    def get_by_name(self, db: Session, name: str) -> Optional[Department]:
        """Get department by name"""
        return db.query(Department).filter(Department.name == name).first()
    
    def get_high_congestion(self, db: Session) -> List[Department]:
        """Get departments with high congestion"""
        return db.query(Department).filter(Department.congestion_level == "High").all()
    
    def update_patient_count(self, db: Session, dept_id: int, count: int) -> Department:
        """Update patient count for a department"""
        dept = self.get(db, dept_id)
        if dept:
            dept.current_patients = count
            # Update congestion level based on patient count
            if count > 20:
                dept.congestion_level = "High"
                dept.estimated_wait_minutes = 30
            elif count > 10:
                dept.congestion_level = "Moderate"
                dept.estimated_wait_minutes = 20
            else:
                dept.congestion_level = "Low"
                dept.estimated_wait_minutes = 10
            db.commit()
            db.refresh(dept)
        return dept


# Create instance
department = CRUDDepartment(Department)

# Made with Bob
