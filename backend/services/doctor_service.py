from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session
from crud import doctor as doctor_crud, appointment as appt_crud
from database.models import Doctor, Appointment

# Mock response for AI scribe fallback
SCRIBE_RESPONSE = {
    "notes": "S: Patient reports intermittent chest tightness for 2 days. O: Vitals stable, ECG pending. A: Suspected angina. P: Start low-dose aspirin, schedule stress test, advise rest.",
    "prescription": [
        {
            "medication": "Aspirin 81mg",
            "dosage": "Once daily",
            "duration": "14 days",
        },
        {
            "medication": "Nitroglycerin 0.4mg",
            "dosage": "As needed",
            "duration": "7 days",
        },
    ],
}

try:
    from config import config
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from config import config


class DoctorService:
    @staticmethod
    def get_all_patients(db: Session):
        """Return every patient with the same summary shape used in the doctor view."""
        from database.models import Patient, Doctor, MedicalRecord, Medication, Appointment, Consultation, Prescription
        from sqlalchemy import desc

        patients = []
        all_patients = db.query(Patient).order_by(Patient.name.asc()).all()

        for patient in all_patients:
            patient_appointments = db.query(Appointment).filter(
                Appointment.patient_id == patient.id
            ).order_by(desc(Appointment.scheduled_time)).all()

            upcoming_candidates = [
                appointment for appointment in patient_appointments
                if appointment.status in ["Scheduled", "In Progress"] and appointment.scheduled_time >= datetime.now()
            ]
            upcoming_appt = min(upcoming_candidates, key=lambda appt: appt.scheduled_time, default=None)
            completed_visits = len([appointment for appointment in patient_appointments if appointment.status == "Completed"])

            medical_records = db.query(MedicalRecord).filter(
                MedicalRecord.patient_id == patient.id
            ).order_by(desc(MedicalRecord.diagnosis_date)).all()

            current_medications = db.query(Medication).filter(
                Medication.patient_id == patient.id,
                Medication.is_active == True
            ).all()

            previous_medications = db.query(Medication).filter(
                Medication.patient_id == patient.id,
                Medication.is_active == False
            ).all()

            latest_consultation = db.query(Consultation).filter(
                Consultation.patient_id == patient.id
            ).order_by(desc(Consultation.consultation_date)).first()

            latest_prescription = db.query(Prescription).filter(
                Prescription.patient_id == patient.id
            ).order_by(desc(Prescription.prescribed_date)).first()

            linked_doctor = None
            if latest_consultation and latest_consultation.doctor:
                linked_doctor = latest_consultation.doctor
            elif patient_appointments and patient_appointments[0].doctor:
                linked_doctor = patient_appointments[0].doctor

            patients.append(
                {
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age or 0,
                    "gender": "Male" if patient.id % 2 == 0 else "Female",
                    "phone": patient.phone,
                    "blood_group": patient.blood_group,
                    "allergies": patient.allergies or "None",
                    "linked_doctor": {
                        "id": linked_doctor.id,
                        "name": linked_doctor.name,
                        "department": linked_doctor.department.name if linked_doctor and linked_doctor.department else "N/A",
                        "specialization": linked_doctor.specialization if linked_doctor else None,
                    } if linked_doctor else None,
                    "visit_history": completed_visits,
                    "upcoming_appointment": {
                        "date": upcoming_appt.scheduled_time.strftime("%Y-%m-%d"),
                        "time": upcoming_appt.scheduled_time.strftime("%I:%M %p"),
                        "complaint": upcoming_appt.complaint,
                        "notes": upcoming_appt.notes,
                    } if upcoming_appt else None,
                    "existing_conditions": [record.diagnosis for record in medical_records[:5]],
                    "current_medications": [
                        {
                            "name": med.medication_name,
                            "dosage": med.dosage,
                            "started": med.started_date.isoformat() if med.started_date else None,
                        }
                        for med in current_medications
                    ],
                    "previous_medications": [
                        {
                            "name": med.medication_name,
                            "dosage": med.dosage,
                            "ended": med.ended_date.isoformat() if med.ended_date else None,
                        }
                        for med in previous_medications[:5]
                    ],
                    "latest_consultation": {
                        "date": latest_consultation.consultation_date.strftime("%Y-%m-%d"),
                        "soap_notes": latest_consultation.soap_notes,
                    } if latest_consultation else None,
                    "latest_prescription": {
                        "date": latest_prescription.prescribed_date.strftime("%Y-%m-%d"),
                        "notes": latest_prescription.notes,
                    } if latest_prescription else None,
                    "summary": {
                        "last_visit": patient_appointments[0].scheduled_time.strftime("%Y-%m-%d") if patient_appointments else "Never",
                        "total_visits": completed_visits,
                        "next_appointment": upcoming_appt.scheduled_time.strftime("%Y-%m-%d %I:%M %p") if upcoming_appt else "None scheduled",
                    },
                }
            )

        return {
            "total": len(patients),
            "patients": patients,
        }

    @staticmethod
    def _build_patient_summary(db: Session, doctor_id: int):
        from database.models import Patient, MedicalRecord, Medication, Appointment, Consultation, Prescription
        from sqlalchemy import desc

        patient_ids = db.query(Appointment.patient_id).filter(
            Appointment.doctor_id == doctor_id
        ).distinct().all()

        patients = []
        for (patient_id,) in patient_ids:
            patient = db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                continue

            patient_appointments = db.query(Appointment).filter(
                Appointment.patient_id == patient.id,
                Appointment.doctor_id == doctor_id
            ).order_by(desc(Appointment.scheduled_time)).all()

            upcoming_candidates = [
                a for a in patient_appointments
                if a.status in ["Scheduled", "In Progress"] and a.scheduled_time >= datetime.now()
            ]
            upcoming_appt = min(upcoming_candidates, key=lambda appt: appt.scheduled_time, default=None)
            completed_visits = len([a for a in patient_appointments if a.status == "Completed"])

            medical_records = db.query(MedicalRecord).filter(
                MedicalRecord.patient_id == patient.id
            ).order_by(desc(MedicalRecord.diagnosis_date)).all()

            current_medications = db.query(Medication).filter(
                Medication.patient_id == patient.id,
                Medication.is_active == True
            ).all()

            previous_medications = db.query(Medication).filter(
                Medication.patient_id == patient.id,
                Medication.is_active == False
            ).all()

            latest_consultation = db.query(Consultation).filter(
                Consultation.patient_id == patient.id,
                Consultation.doctor_id == doctor_id
            ).order_by(desc(Consultation.consultation_date)).first()

            latest_prescription = db.query(Prescription).filter(
                Prescription.patient_id == patient.id,
                Prescription.doctor_id == doctor_id
            ).order_by(desc(Prescription.prescribed_date)).first()

            patients.append(
                {
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age or 0,
                    "gender": "Male" if patient.id % 2 == 0 else "Female",
                    "phone": patient.phone,
                    "blood_group": patient.blood_group,
                    "allergies": patient.allergies or "None",
                    "visit_history": completed_visits,
                    "upcoming_appointment": {
                        "date": upcoming_appt.scheduled_time.strftime("%Y-%m-%d"),
                        "time": upcoming_appt.scheduled_time.strftime("%I:%M %p"),
                        "complaint": upcoming_appt.complaint,
                        "notes": upcoming_appt.notes,
                    } if upcoming_appt else None,
                    "existing_conditions": [record.diagnosis for record in medical_records[:5]],
                    "current_medications": [
                        {
                            "name": med.medication_name,
                            "dosage": med.dosage,
                            "started": med.started_date.isoformat() if med.started_date else None,
                        }
                        for med in current_medications
                    ],
                    "previous_medications": [
                        {
                            "name": med.medication_name,
                            "dosage": med.dosage,
                            "ended": med.ended_date.isoformat() if med.ended_date else None,
                        }
                        for med in previous_medications[:5]
                    ],
                    "latest_consultation": {
                        "date": latest_consultation.consultation_date.strftime("%Y-%m-%d"),
                        "soap_notes": latest_consultation.soap_notes,
                    } if latest_consultation else None,
                    "latest_prescription": {
                        "date": latest_prescription.prescribed_date.strftime("%Y-%m-%d"),
                        "notes": latest_prescription.notes,
                    } if latest_prescription else None,
                    "summary": {
                        "last_visit": patient_appointments[0].scheduled_time.strftime("%Y-%m-%d") if patient_appointments else "Never",
                        "total_visits": completed_visits,
                        "next_appointment": upcoming_appt.scheduled_time.strftime("%Y-%m-%d %I:%M %p") if upcoming_appt else "None scheduled",
                    },
                }
            )

        return patients

    @staticmethod
    def get_doctor_dashboard(db: Session, doctor_id: int = None):
        """Get doctor dashboard data"""
        # If no doctor_id provided, get first doctor (for demo)
        if not doctor_id:
            doctor = db.query(Doctor).first()
        else:
            doctor = doctor_crud.get(db, doctor_id)
        
        if not doctor:
            return {"error": "Doctor not found"}
        
        from sqlalchemy import desc
        from database.models import Consultation, Prescription

        appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor.id).order_by(desc(Appointment.scheduled_time)).all()
        today = datetime.now().date()
        today_appointments = [a for a in appointments if a.scheduled_time.date() == today]
        completed = len([a for a in today_appointments if a.status == "Completed"])
        pending = len([a for a in today_appointments if a.status in ["Scheduled", "In Progress"]])

        next_candidates = [
            a for a in appointments
            if a.status in ["Scheduled", "In Progress"] and a.scheduled_time >= datetime.now()
        ]
        next_appt = min(next_candidates, key=lambda appt: appt.scheduled_time, default=None)
        patients = DoctorService._build_patient_summary(db, doctor.id)
        recent_consultations = db.query(Consultation).filter(Consultation.doctor_id == doctor.id).order_by(desc(Consultation.consultation_date)).limit(5).all()
        recent_prescriptions = db.query(Prescription).filter(Prescription.doctor_id == doctor.id).order_by(desc(Prescription.prescribed_date)).limit(5).all()
        
        return {
            "doctor": doctor.to_dict(),
            "appointments_today": len(today_appointments),
            "completed": completed,
            "pending": pending,
            "today_appointments": [
                {
                    "id": appt.id,
                    "time": appt.scheduled_time.strftime("%I:%M %p"),
                    "date": appt.scheduled_time.strftime("%Y-%m-%d"),
                    "status": appt.status,
                    "patient": appt.patient.name if appt.patient else "N/A",
                    "reason": appt.complaint,
                    "notes": appt.notes,
                }
                for appt in today_appointments
            ],
            "next_patient": {
                "name": next_appt.patient.name if next_appt and next_appt.patient else "No patients",
                "age": next_appt.patient.age if next_appt and next_appt.patient else 0,
                "complaint": next_appt.complaint if next_appt else "N/A",
            } if next_appt else None,
            "assigned_patients": patients,
            "recent_consultations": [
                {
                    "id": consult.id,
                    "patient": consult.patient.name if consult.patient else "N/A",
                    "date": consult.consultation_date.strftime("%Y-%m-%d"),
                    "soap_notes": consult.soap_notes,
                }
                for consult in recent_consultations
            ],
            "recent_prescriptions": [
                {
                    "id": prescription.id,
                    "patient": prescription.patient.name if prescription.patient else "N/A",
                    "date": prescription.prescribed_date.strftime("%Y-%m-%d"),
                    "notes": prescription.notes,
                    "medications": [item.to_dict() for item in prescription.items],
                }
                for prescription in recent_prescriptions
            ],
        }

    @staticmethod
    def get_doctor_patients(db: Session, doctor_id: int = None):
        """Get doctor's patient list with comprehensive details"""
        # If no doctor_id provided, get first doctor (for demo)
        if not doctor_id:
            doctor = db.query(Doctor).first()
        else:
            doctor = doctor_crud.get(db, doctor_id)
        
        if not doctor:
            return {"error": "Doctor not found"}
        
        patients = DoctorService._build_patient_summary(db, doctor.id)

        return {"doctor": doctor.to_dict(), "patients": patients, "total": len(patients)}

    @staticmethod
    def post_doctor_scribe(transcript: str, patient_info: Optional[Dict] = None):
        """
        Process consultation transcript and generate notes and prescription
        
        Args:
            transcript: Consultation transcript (can be pre-formatted or raw)
            patient_info: Optional patient information for prescription
            
        Returns:
            Dict containing notes, prescription, and extracted entities
        """
        # Check if Gemini is configured for AI processing
        if not config.is_gemini_configured():
            # Return mock data if not configured
            return {
                "notes": SCRIBE_RESPONSE["notes"],
                "prescription": SCRIBE_RESPONSE["prescription"],
                "received_transcript": transcript,
                "mode": "mock",
                "message": "Using mock data. Configure the Gemini API key in .env for AI processing."
            }
        
        try:
            try:
                from medical_ai_service import get_medical_ai_service
            except ImportError:
                from services.medical_ai_service import get_medical_ai_service
            
            ai_service = get_medical_ai_service()

            analysis = ai_service.get_consultation_analysis(transcript, patient_info)
            entities = analysis.get("entities", {})
            soap_notes = analysis.get("soap_notes", "")
            prescription_data = analysis.get("prescription", {})
            quality_analysis = analysis.get("quality_analysis", {})

            if not soap_notes:
                soap_notes = ai_service.generate_soap_notes(transcript, entities)
            if not prescription_data:
                prescription_data = ai_service.generate_prescription(transcript, entities, patient_info)
            if not quality_analysis:
                quality_analysis = ai_service.analyze_transcript_quality(transcript)
            
            return {
                "notes": soap_notes,
                "prescription": prescription_data["medications"],
                "full_prescription": prescription_data,
                "entities": entities,
                "quality_analysis": quality_analysis,
                "received_transcript": transcript,
                "mode": "ai" if analysis.get("analysis_source") != "local_fallback" else "fallback",
                "analysis_source": analysis.get("analysis_source", "gemini"),
            }
        
        except Exception as e:
            # Fallback to mock data on error
            return {
                "notes": SCRIBE_RESPONSE["notes"],
                "prescription": SCRIBE_RESPONSE["prescription"],
                "received_transcript": transcript,
                "mode": "mock",
                "error": str(e),
                "message": "AI processing failed. Using mock data."
            }
    
    @staticmethod
    def process_audio_transcription(audio_file_path: str, patient_info: Optional[Dict] = None):
        """
        Process audio file: transcribe and generate medical documents
        
        Args:
            audio_file_path: Path to audio file
            patient_info: Optional patient information
            
        Returns:
            Dict containing transcript, notes, and prescription
        """
        if not config.is_gemini_configured() or not config.is_speech_configured():
            return {
                "error": "API keys not configured",
                "message": "Please configure IBM Watson or Grok/Groq, plus Gemini, in the .env file"
            }
        
        try:
            try:
                from speech_to_text_service import get_speech_service
                from medical_ai_service import get_medical_ai_service
            except ImportError:
                from services.speech_to_text_service import get_speech_service
                from services.medical_ai_service import get_medical_ai_service
            
            # Transcribe audio
            speech_service = get_speech_service()
            transcription_result = speech_service.transcribe_audio_file(audio_file_path)
            
            # Use formatted transcript for AI processing
            formatted_transcript = transcription_result["formatted_transcript"]
            
            # Process with AI
            ai_service = get_medical_ai_service()
            analysis = ai_service.get_consultation_analysis(formatted_transcript, patient_info)
            entities = analysis.get("entities", {})
            soap_notes = analysis.get("soap_notes", "") or ai_service.generate_soap_notes(formatted_transcript, entities)
            prescription_data = analysis.get("prescription", {}) or ai_service.generate_prescription(formatted_transcript, entities, patient_info)
            
            return {
                "transcription": transcription_result,
                "notes": soap_notes,
                "prescription": prescription_data["medications"],
                "full_prescription": prescription_data,
                "entities": entities,
                "mode": "ai" if analysis.get("analysis_source") != "local_fallback" else "fallback",
                "analysis_source": analysis.get("analysis_source", "gemini"),
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "message": "Error processing audio file"
            }


# Made with Bob
