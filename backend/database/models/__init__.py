"""
Database models for MediFlow OS
"""

from .department import Department
from .doctor import Doctor
from .patient import Patient
from .appointment import Appointment
from .queue import QueueEntry
from .consultation import Consultation
from .prescription import Prescription, PrescriptionItem
from .medical_record import MedicalRecord, Medication, LabResult, Vaccination

__all__ = [
    "Department",
    "Doctor",
    "Patient",
    "Appointment",
    "QueueEntry",
    "Consultation",
    "Prescription",
    "PrescriptionItem",
    "MedicalRecord",
    "Medication",
    "LabResult",
    "Vaccination",
]

# Made with Bob
