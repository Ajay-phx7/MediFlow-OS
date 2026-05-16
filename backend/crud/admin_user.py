"""
CRUD operations for AdminUser model
"""

from sqlalchemy.orm import Session
from database.models import AdminUser


def create(db: Session, username: str, department: str) -> AdminUser:
    """Create a new admin user"""
    admin = AdminUser(username=username, department=department)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def get_all(db: Session):
    """Get all admin users"""
    return db.query(AdminUser).all()


def get_by_id(db: Session, admin_id: int):
    """Get admin user by ID"""
    return db.query(AdminUser).filter(AdminUser.id == admin_id).first()


def get_by_username(db: Session, username: str):
    """Get admin user by username"""
    return db.query(AdminUser).filter(AdminUser.username == username).first()


def get_by_department(db: Session, department: str):
    """Get admin user by department"""
    return db.query(AdminUser).filter(AdminUser.department == department).first()


# Made with Bob