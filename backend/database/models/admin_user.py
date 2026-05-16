"""
Admin User model for MediFlow OS
Represents admin accounts for different departments
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.connection import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    department = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert admin user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "department": self.department,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }

    def __repr__(self):
        return f"<AdminUser(id={self.id}, username='{self.username}', department='{self.department}')>"


# Made with Bob