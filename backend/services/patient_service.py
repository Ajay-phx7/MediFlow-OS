from sqlalchemy.orm import Session
from sqlalchemy import desc
from crud import patient as patient_crud, appointment as appt_crud
from database.models import (
    Patient, Medication, MedicalRecord, LabResult, Vaccination,
    Appointment, Prescription, Consultation
)


class PatientService:
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
        
        # Get upcoming appointments
        from datetime import datetime
        upcoming_appointments = sorted(
            [a for a in all_appointments if a.scheduled_time > datetime.now() and a.status == "Scheduled"],
            key=lambda appt: appt.scheduled_time,
        )
        
        # Get past appointments
        past_appointments = [
            a for a in all_appointments
            if a.status == "Completed"
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
                    "doctor": appt.doctor.name if appt.doctor else "N/A",
                    "department": appt.doctor.department.name if appt.doctor and appt.doctor.department else "N/A",
                    "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                    "time": appt.scheduled_time.strftime("%I:%M %p"),
                    "complaint": appt.complaint,
                    "status": appt.status,
                    "notes": appt.notes,
                }
                for appt in upcoming_appointments[:3]
            ],
            "past_appointments": [
                {
                    "id": appt.id,
                    "doctor": appt.doctor.name if appt.doctor else "N/A",
                    "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                    "complaint": appt.complaint,
                    "status": appt.status,
                    "notes": appt.notes,
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
                    "soap_notes": c.soap_notes,
                    "notes": c.soap_notes[:200] + "..." if c.soap_notes and len(c.soap_notes) > 200 else c.soap_notes
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


# Made with Bob
