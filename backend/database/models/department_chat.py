"""
Department Chat Message model for MediFlow OS
Stores chat messages between admin users in different departments
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database.connection import Base


class DepartmentChatMessage(Base):
    __tablename__ = "department_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False, index=True)
    sender_username = Column(String, nullable=False)
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        """Convert chat message to dictionary"""
        return {
            "id": self.id,
            "department": self.department,
            "sender_username": self.sender_username,
            "message_text": self.message_text,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self):
        return f"<DepartmentChatMessage(id={self.id}, department='{self.department}', sender='{self.sender_username}')>"


# Made with Bob