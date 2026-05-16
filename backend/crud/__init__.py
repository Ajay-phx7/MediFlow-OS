"""
CRUD operations for MediFlow OS database
"""

from .base import CRUDBase
from .department import department
from .doctor import doctor
from .patient import patient
from .appointment import appointment
from .queue import queue

__all__ = [
    "CRUDBase",
    "department",
    "doctor",
    "patient",
    "appointment",
    "queue",
]

# Made with Bob
