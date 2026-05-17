from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, date
from typing import Optional, List, Dict
from crud import patient as patient_crud, appointment as appt_crud, doctor as doctor_crud
from database.models import (
    Patient, Medication, MedicalRecord, LabResult, Vaccination,
    Appointment, Prescription, Consultation, Doctor
)


class PatientService:
    @staticmethod
    def _serialize_patient(patient: Patient):
        return {
            "id": patient.id,
            "name": patient.name,
            "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            "age": patient.age,
            "blood_group": patient.blood_group,
            "allergies": patient.allergies,
            "phone": patient.phone,
            "email": patient.email,
            "address": patient.address,
        }

    @staticmethod
    def signup_patient(db: Session, payload: Dict) -> Dict:
        """Create a new patient profile for public signup"""
        if payload.get("email") and patient_crud.get_by_email(db, payload["email"]):
            return {"error": "A patient with this email already exists"}

        if payload.get("phone") and patient_crud.get_by_phone(db, payload["phone"]):
            return {"error": "A patient with this phone already exists"}

        patient = patient_crud.create(
            db,
            name=payload["name"],
            date_of_birth=payload.get("date_of_birth"),
            age=payload.get("age"),
            blood_group=payload.get("blood_group"),
            allergies=payload.get("allergies"),
            phone=payload.get("phone"),
            email=payload.get("email"),
            address=payload.get("address"),
        )

        return {
            "success": True,
            "message": f"Welcome, {patient.name}! Your profile has been created.",
            "patient": PatientService._serialize_patient(patient),
        }

    @staticmethod
    def get_patient_dashboard(db: Session, patient_id: int = None):
        """Get comprehensive patient dashboard data"""
        # If no patient_id provided, get first patient (for demo)
        if not patient_id:
            patient = db.query(Patient).first()
        else:
            patient = patient_crud.get(db, patient_id)
        
        if not patient:
            return {"error": "Patient not found"}
        
        # Get all appointments
        all_appointments = db.query(Appointment).filter(
            Appointment.patient_id == patient.id
        ).order_by(desc(Appointment.scheduled_time)).all()
        
        # Get upcoming and past appointments by date
        today = date.today()
        upcoming_appointments = sorted(
            [a for a in all_appointments if a.scheduled_time.date() >= today],
            key=lambda appt: appt.scheduled_time,
        )

        past_appointments = [
            a for a in all_appointments
            if a.scheduled_time.date() < today
        ]
        
        # Get current medications
        medications = db.query(Medication).filter(
            Medication.patient_id == patient.id,
            Medication.is_active == True
        ).all()
        
        # Get prescriptions
        prescriptions = db.query(Prescription).filter(
            Prescription.patient_id == patient.id
        ).order_by(desc(Prescription.prescribed_date)).limit(5).all()
        
        # Get consultations
        consultations = db.query(Consultation).filter(
            Consultation.patient_id == patient.id
        ).order_by(desc(Consultation.consultation_date)).limit(5).all()

        linked_doctor = None
        if consultations and consultations[0].doctor:
            linked_doctor = consultations[0].doctor
        elif all_appointments and all_appointments[0].doctor:
            linked_doctor = all_appointments[0].doctor

        diagnoses = db.query(MedicalRecord).filter(
            MedicalRecord.patient_id == patient.id
        ).order_by(desc(MedicalRecord.diagnosis_date)).all()

        diagnosis_history = [
            {
                "diagnosis": record.diagnosis,
                "date": record.diagnosis_date.isoformat() if record.diagnosis_date else None,
                "notes": record.notes,
            }
            for record in diagnoses[:10]
        ]
        
        return {
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "blood_group": patient.blood_group,
                "allergies": patient.allergies,
                "phone": patient.phone,
                "email": patient.email
            },
            "linked_doctor": {
                "id": linked_doctor.id,
                "name": linked_doctor.name,
                "department": linked_doctor.department.name if linked_doctor.department else "N/A",
                "specialization": linked_doctor.specialization,
            } if linked_doctor else None,
            "upcoming_appointments": [
                {
                    "id": appt.id,
                    "doctor_id": appt.doctor_id,
                    "doctor": appt.doctor.name if appt.doctor else "N/A",
                    "department": appt.doctor.department.name if appt.doctor and appt.doctor.department else "N/A",
                    "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                    "time": appt.scheduled_time.strftime("%I:%M %p"),
                    "scheduled_time": appt.scheduled_time.isoformat() if appt.scheduled_time else None,
                    "complaint": appt.complaint,
                    "status": appt.get_computed_status(),
                    # Notes excluded for patient privacy - only doctors can see notes
                }
                for appt in upcoming_appointments[:3]
            ],
            "past_appointments": [
                {
                    "id": appt.id,
                    "doctor_id": appt.doctor_id,
                    "doctor": appt.doctor.name if appt.doctor else "N/A",
                    "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                    "complaint": appt.complaint,
                    "status": appt.get_computed_status(),
                    # Notes excluded for patient privacy - only doctors can see notes
                }
                for appt in past_appointments[:5]
            ],
            "current_medications": [
                {
                    "name": m.medication_name,
                    "dosage": m.dosage,
                    "started": m.started_date.isoformat() if m.started_date else None
                }
                for m in medications
            ],
            "recent_prescriptions": [
                {
                    "id": p.id,
                    "doctor": p.doctor.name if p.doctor else "N/A",
                    "date": p.prescribed_date.strftime("%Y-%m-%d"),
                    "medications": [
                        {
                            "name": item.medication_name,
                            "dosage": item.dosage,
                            "frequency": item.frequency,
                            "duration": item.duration
                        }
                        for item in p.items
                    ]
                }
                for p in prescriptions
            ],
            "recent_consultations": [
                {
                    "id": c.id,
                    "doctor": c.doctor.name if c.doctor else "N/A",
                    "date": c.consultation_date.strftime("%Y-%m-%d"),
                    # SOAP notes excluded for patient privacy - only doctors can see detailed consultation notes
                    "summary": "Consultation completed"
                }
                for c in consultations
            ],
            "diagnosis_history": diagnosis_history,
        }

    @staticmethod
    def get_health_report(db: Session, patient_id: int = None):
        """Get patient health report"""
        # If no patient_id provided, get first patient (for demo)
        if not patient_id:
            patient = db.query(Patient).first()
        else:
            patient = patient_crud.get(db, patient_id)
        
        if not patient:
            return {"error": "Patient not found"}
        
        # Get medical data
        medications = db.query(Medication).filter(
            Medication.patient_id == patient.id,
            Medication.is_active == True
        ).all()
        
        diagnoses = db.query(MedicalRecord).filter(
            MedicalRecord.patient_id == patient.id
        ).order_by(MedicalRecord.diagnosis_date.desc()).all()
        
        lab_results = db.query(LabResult).filter(
            LabResult.patient_id == patient.id
        ).order_by(LabResult.test_date.desc()).limit(10).all()
        
        vaccinations = db.query(Vaccination).filter(
            Vaccination.patient_id == patient.id
        ).order_by(Vaccination.vaccination_date.desc()).all()
        
        return {
            "summary": {
                "name": patient.name,
                "dob": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                "blood_group": patient.blood_group,
                "allergies": patient.allergies,
            },
            "current_medications": [f"{m.medication_name} {m.dosage}" for m in medications],
            "past_diagnoses": [
                {
                    "diagnosis": d.diagnosis,
                    "date": d.diagnosis_date.isoformat() if d.diagnosis_date else None,
                    "notes": d.notes,
                }
                for d in diagnoses
            ],
            "recent_lab_results": [
                {
                    "test": r.test_name,
                    "value": r.value,
                    "date": r.test_date.isoformat() if r.test_date else None
                } for r in lab_results
            ],
            "vaccinations": [
                f"{v.vaccine_name} ({v.vaccination_date.year})" for v in vaccinations
            ],
        }
    
    @staticmethod
    def get_available_doctors(db: Session) -> List[Dict]:
        """Get list of all available doctors for appointment booking"""
        doctors = db.query(Doctor).filter(Doctor.is_available == True).all()
        return [
            {
                "id": doctor.id,
                "name": doctor.name,
                "specialization": doctor.specialization,
                "department": doctor.department.name if doctor.department else "N/A",
                "department_id": doctor.department_id
            }
            for doctor in doctors
        ]
    
    @staticmethod
    def get_available_slots(db: Session, doctor_id: int, appointment_date: str) -> Dict:
        """
        Get available time slots for a doctor on a specific date
        
        Args:
            db: Database session
            doctor_id: ID of the doctor
            appointment_date: Date in YYYY-MM-DD format
            
        Returns:
            Dict with doctor info and available slots
        """
        doctor = doctor_crud.get(db, doctor_id)
        if not doctor:
            return {"error": "Doctor not found"}
        
        try:
            target_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        # Don't allow booking for past dates
        if target_date < date.today():
            return {"error": "Cannot book appointments for past dates"}
        
        available_slots = appt_crud.get_available_slots(db, doctor_id, target_date)
        
        return {
            "doctor": {
                "id": doctor.id,
                "name": doctor.name,
                "specialization": doctor.specialization,
                "department": doctor.department.name if doctor.department else "N/A"
            },
            "date": appointment_date,
            "available_slots": available_slots
        }
    
    @staticmethod
    def book_appointment(
        db: Session,
        patient_id: int,
        doctor_id: int,
        appointment_date: str,
        appointment_time: str,
        complaint: Optional[str] = None
    ) -> Dict:
        """
        Book an appointment for a patient
        
        Args:
            db: Database session
            patient_id: ID of the patient
            doctor_id: ID of the doctor
            appointment_date: Date in YYYY-MM-DD format
            appointment_time: Time in HH:MM format
            complaint: Optional complaint/reason for visit
            
        Returns:
            Dict with appointment details or error
        """
        # Validate patient
        patient = patient_crud.get(db, patient_id)
        if not patient:
            return {"error": "Patient not found"}
        
        # Validate doctor
        doctor = doctor_crud.get(db, doctor_id)
        if not doctor:
            return {"error": "Doctor not found"}
        
        # Parse and validate date/time
        try:
            target_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            target_time = datetime.strptime(appointment_time, "%H:%M").time()
            scheduled_datetime = datetime.combine(target_date, target_time)
        except ValueError:
            return {"error": "Invalid date or time format"}
        
        # Don't allow booking for past dates/times
        if scheduled_datetime < datetime.now():
            return {"error": "Cannot book appointments in the past"}
        
        # Prevent duplicate appointments for the same patient on the same date
        day_start = datetime.combine(target_date, datetime.min.time())
        day_end = datetime.combine(target_date, datetime.max.time())
        existing_patient_appt = db.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.scheduled_time >= day_start,
            Appointment.scheduled_time <= day_end,
            Appointment.status != "Cancelled"
        ).first()
        if existing_patient_appt:
            return {"error": "Patient already has an appointment on this date"}

        # Check if slot is available
        available_slots = appt_crud.get_available_slots(db, doctor_id, target_date)
        if appointment_time not in available_slots:
            return {"error": "Selected time slot is not available"}
        
        # Create appointment
        appointment = appt_crud.create_appointment(
            db=db,
            patient_id=patient_id,
            doctor_id=doctor_id,
            scheduled_time=scheduled_datetime,
            complaint=complaint
        )
        
        return {
            "success": True,
            "message": "Appointment booked successfully",
            "appointment": {
                "id": appointment.id,
                "patient_name": patient.name,
                "doctor_name": doctor.name,
                "doctor_specialization": doctor.specialization,
                "department": doctor.department.name if doctor.department else "N/A",
                "date": appointment_date,
                "time": appointment_time,
                "status": appointment.status,
                "complaint": appointment.complaint
            }
        }
    
    @staticmethod
    def get_patient_appointments(db: Session, patient_id: int) -> Dict:
        """
        Get all appointments for a patient with computed status
        
        Args:
            db: Database session
            patient_id: ID of the patient
            
        Returns:
            Dict with upcoming and past appointments
        """
        patient = patient_crud.get(db, patient_id)
        if not patient:
            return {"error": "Patient not found"}
        
        all_appointments = appt_crud.get_by_patient(db, patient_id)
        
        today = date.today()
        upcoming = []
        past = []
        
        for appt in all_appointments:
            appt_date = appt.scheduled_time.date()
            computed_status = appt.get_computed_status()
            
            appt_dict = {
                "id": appt.id,
                "doctor_name": appt.doctor.name if appt.doctor else "N/A",
                "doctor_specialization": appt.doctor.specialization if appt.doctor else "N/A",
                "department": appt.doctor.department.name if appt.doctor and appt.doctor.department else "N/A",
                "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                "time": appt.scheduled_time.strftime("%I:%M %p"),
                "status": computed_status,
                "complaint": appt.complaint
                # Notes field excluded - only doctors can see appointment notes
            }
            
            if appt_date >= today:
                upcoming.append(appt_dict)
            else:
                past.append(appt_dict)
        
        return {
            "patient": {
                "id": patient.id,
                "name": patient.name
            },
            "upcoming_appointments": sorted(upcoming, key=lambda x: x["date"]),
            "past_appointments": sorted(past, key=lambda x: x["date"], reverse=True)
        }

    @staticmethod
    def cancel_appointment(db: Session, patient_id: int, appointment_id: int) -> Dict:
        """Cancel one of the patient's future appointments"""
        appointment = appt_crud.get(db, appointment_id)
        if not appointment:
            return {"error": "Appointment not found"}

        if appointment.patient_id != patient_id:
            return {"error": "Access denied"}

        if appointment.status == "Cancelled":
            return {"error": "Appointment is already cancelled"}

        if appointment.status == "Completed" or appointment.scheduled_time <= datetime.now():
            return {"error": "Only future appointments can be cancelled"}

        updated = appt_crud.cancel_appointment(db, appointment_id)
        return {
            "success": True,
            "message": "Appointment cancelled successfully",
            "appointment": updated.to_dict(include_computed_status=True) if updated else None,
        }

    @staticmethod
    def reschedule_appointment(
        db: Session,
        patient_id: int,
        appointment_id: int,
        appointment_date: str,
        appointment_time: str,
    ) -> Dict:
        """Reschedule one of the patient's future appointments"""
        appointment = appt_crud.get(db, appointment_id)
        if not appointment:
            return {"error": "Appointment not found"}

        if appointment.patient_id != patient_id:
            return {"error": "Access denied"}

        if appointment.status in ["Cancelled", "Completed"] or appointment.scheduled_time <= datetime.now():
            return {"error": "Only future appointments can be rescheduled"}

        try:
            target_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            target_time = datetime.strptime(appointment_time, "%H:%M").time()
            scheduled_datetime = datetime.combine(target_date, target_time)
        except ValueError:
            return {"error": "Invalid date or time format"}

        if scheduled_datetime <= datetime.now():
            return {"error": "Reschedule time must be in the future"}

        available_slots = appt_crud.get_available_slots(
            db,
            appointment.doctor_id,
            target_date,
            exclude_appointment_id=appointment.id,
        )
        if appointment_time not in available_slots:
            return {"error": "Selected time slot is not available"}

        updated = appt_crud.reschedule_appointment(db, appointment_id, scheduled_datetime)
        return {
            "success": True,
            "message": "Appointment rescheduled successfully",
            "appointment": updated.to_dict(include_computed_status=True) if updated else None,
        }


# Made with Bob
