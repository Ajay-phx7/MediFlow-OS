"""
Weekly Report Mock Data for MediFlow-OS
Provides comprehensive hospital metrics, clinical data, and safety compliance data
"""

# All data hardcoded for MVP (no database)

WEEKLY_REPORT_DATA = {
    # Basic Report Info
    "report_week": "May 12-18, 2024",
    "generated_date": "2024-05-19",
    "hospital_name": "City General Hospital",
    
    # ════════════════════════════════════════
    # HOSPITAL METRICS (Executive Summary)
    # ════════════════════════════════════════
    "hospital_metrics": {
        "total_patients": 1245,
        "patient_change_percent": 12,
        "new_patients_admitted": 450,
        "patients_discharged": 420,
        "emergency_walk_ins": 125,
        "scheduled_appointments": 980,
        
        "avg_wait_time_minutes": 24,
        "wait_time_change_minutes": -3,
        "emergency_wait_time_minutes": 35,
        "opd_wait_time_minutes": 22,
        "lab_wait_time_minutes": 150,
        "pharmacy_wait_time_minutes": 8,
        
        "bed_occupancy_percent": 87,
        "occupancy_change_percent": 5,
        "total_beds": 150,
        "occupied_beds": 130,
        "available_beds": 20,
        
        "no_show_rate_percent": 5.2,
        "readmission_rate_percent": 3.1,
        "patient_satisfaction_rating": 4.3
    },
    
    # ════════════════════════════════════════
    # DEPARTMENT PERFORMANCE
    # ════════════════════════════════════════
    "department_stats": [
        {
            "department": "Emergency",
            "patients": 125,
            "avg_wait_minutes": 35,
            "bed_occupancy_percent": 92,
            "beds_occupied": 15,
            "total_beds": 15,
            "rating": 4.1,
            "status": "High Utilization",
            "trend": "up"
        },
        {
            "department": "Cardiology",
            "patients": 89,
            "avg_wait_minutes": 18,
            "bed_occupancy_percent": 76,
            "beds_occupied": 12,
            "total_beds": 16,
            "rating": 4.5,
            "status": "Optimal",
            "trend": "stable"
        },
        {
            "department": "Orthopedics",
            "patients": 67,
            "avg_wait_minutes": 15,
            "bed_occupancy_percent": 65,
            "beds_occupied": 10,
            "total_beds": 15,
            "rating": 4.3,
            "status": "Good",
            "trend": "stable"
        },
        {
            "department": "Pediatrics",
            "patients": 112,
            "avg_wait_minutes": 20,
            "bed_occupancy_percent": 88,
            "beds_occupied": 14,
            "total_beds": 16,
            "rating": 4.6,
            "status": "High Utilization",
            "trend": "up"
        },
        {
            "department": "ICU",
            "patients": 34,
            "avg_wait_minutes": 0,
            "bed_occupancy_percent": 91,
            "beds_occupied": 18,
            "total_beds": 20,
            "rating": 4.4,
            "status": "High Utilization",
            "trend": "up"
        },
        {
            "department": "OPD",
            "patients": 345,
            "avg_wait_minutes": 22,
            "bed_occupancy_percent": 78,
            "beds_occupied": 39,
            "total_beds": 50,
            "rating": 4.0,
            "status": "Good",
            "trend": "stable"
        }
    ],
    
    # ════════════════════════════════════════
    # CLINICAL DATA
    # ════════════════════════════════════════
    "clinical_summary": {
        "total_surgeries": 18,
        "emergency_surgeries": 4,
        "elective_surgeries": 14,
        "surgery_success_rate_percent": 100,
        "post_op_infections": 0,
        "surgical_complications": 0,
        
        "top_diagnoses": [
            {
                "diagnosis": "Hypertension",
                "count": 120,
                "percentage": 9.6
            },
            {
                "diagnosis": "Diabetes",
                "count": 95,
                "percentage": 7.6
            },
            {
                "diagnosis": "Respiratory Infection",
                "count": 87,
                "percentage": 7.0
            },
            {
                "diagnosis": "Fractures",
                "count": 56,
                "percentage": 4.5
            },
            {
                "diagnosis": "Gastroenteritis",
                "count": 45,
                "percentage": 3.6
            },
            {
                "diagnosis": "Others",
                "count": 842,
                "percentage": 67.7
            }
        ],
        
        "lab_tests": {
            "total_tests": 732,
            "blood_tests": 420,
            "imaging_tests": 156,
            "ultrasound": 89,
            "ecg": 67,
            "average_turnaround_hours": 2.5
        },
        
        "medication_usage": {
            "total_prescriptions": 345,
            "average_drugs_per_patient": 2.3,
            "antibiotics_prescribed": 89,
            "controlled_substances": 12
        }
    },
    
    # ════════════════════════════════════════
    # RESOURCE UTILIZATION
    # ════════════════════════════════════════
    "resource_utilization": {
        "beds": {
            "total": 150,
            "occupied": 130,
            "available": 20,
            "occupancy_percent": 87,
            "emergency_beds": 15,
            "emergency_occupied": 15,
            "icu_beds": 20,
            "icu_occupied": 18,
            "general_ward_beds": 75,
            "general_ward_occupied": 58,
            "isolation_beds": 40,
            "isolation_occupied": 39
        },
        
        "equipment": {
            "ventilators": {
                "total": 15,
                "in_use": 12,
                "available": 3
            },
            "monitors": {
                "total": 50,
                "in_use": 45,
                "available": 5
            },
            "wheelchairs": {
                "total": 25,
                "in_use": 17,
                "available": 8
            },
            "stretchers": {
                "total": 22,
                "in_use": 20,
                "available": 2
            },
            "defibrillators": {
                "total": 6,
                "in_use": 2,
                "available": 4
            }
        },
        
        "staffing": {
            "doctors": {
                "total": 20,
                "on_duty": 18,
                "on_leave": 2
            },
            "nurses": {
                "total": 50,
                "on_duty": 45,
                "on_leave": 5
            },
            "support_staff": {
                "total": 15,
                "on_duty": 12,
                "on_leave": 3
            },
            "critical_shortage": False
        }
    },
    
    # ════════════════════════════════════════
    # SAFETY & COMPLIANCE
    # ════════════════════════════════════════
    "safety_compliance": {
        "incidents": {
            "patient_falls": 0,
            "medication_errors": 1,
            "needle_stick_injuries": 0,
            "adverse_events": 2,
            "complaints_filed": 3,
            "severity_levels": {
                "critical": 0,
                "high": 1,
                "medium": 2,
                "low": 0
            }
        },
        
        "data_security": {
            "hipaa_compliance_percent": 95,
            "unauthorized_access_attempts": 0,
            "data_breach_incidents": 0,
            "staff_training_completed_percent": 95,
            "security_audits_passed": True,
            "last_security_audit_date": "2024-05-15"
        },
        
        "infection_control": {
            "hospital_acquired_infections": 0,
            "post_op_infections": 0,
            "antibiotic_resistance_cases": 0,
            "hand_hygiene_compliance_percent": 98,
            "ppe_stock_sufficient": True
        },
        
        "quality_metrics": {
            "infection_rate_percent": 0.0,
            "mortality_rate_percent": 0.5,
            "readmission_rate_percent": 3.1,
            "average_length_of_stay_days": 4.2,
            "surgical_site_infection_percent": 0.0
        },
        
        "regulatory": {
            "norms_compliant": True,
            "license_valid": True,
            "accreditation_current": True,
            "last_inspection": "2024-03-20",
            "violations": 0,
            "pending_certifications": 0
        }
    },
    
    # ════════════════════════════════════════
    # DAILY PATIENT VOLUME TREND (7 days)
    # ════════════════════════════════════════
    "daily_trends": {
        "volume_by_day": [
            {
                "date": "2024-05-12",
                "day": "Friday",
                "total_patients": 165,
                "avg_wait_minutes": 28,
                "bed_occupancy_percent": 82
            },
            {
                "date": "2024-05-13",
                "day": "Saturday",
                "total_patients": 182,
                "avg_wait_minutes": 26,
                "bed_occupancy_percent": 84
            },
            {
                "date": "2024-05-14",
                "day": "Sunday",
                "total_patients": 198,
                "avg_wait_minutes": 24,
                "bed_occupancy_percent": 88
            },
            {
                "date": "2024-05-15",
                "day": "Monday",
                "total_patients": 175,
                "avg_wait_minutes": 22,
                "bed_occupancy_percent": 86
            },
            {
                "date": "2024-05-16",
                "day": "Tuesday",
                "total_patients": 165,
                "avg_wait_minutes": 20,
                "bed_occupancy_percent": 85
            },
            {
                "date": "2024-05-17",
                "day": "Wednesday",
                "total_patients": 190,
                "avg_wait_minutes": 25,
                "bed_occupancy_percent": 89
            },
            {
                "date": "2024-05-18",
                "day": "Thursday",
                "total_patients": 170,
                "avg_wait_minutes": 23,
                "bed_occupancy_percent": 87
            }
        ]
    },
    
    # ════════════════════════════════════════
    # ACTION ITEMS & ALERTS
    # ════════════════════════════════════════
    "action_items": [
        {
            "id": 1,
            "title": "Wheelchair inventory low",
            "priority": "High",
            "status": "Open",
            "due_date": "2024-05-25",
            "action": "Order 20 more units",
            "department": "Facilities"
        },
        {
            "id": 2,
            "title": "Emergency wait times high",
            "priority": "High",
            "status": "In Progress",
            "due_date": "2024-06-01",
            "action": "Hire 2 additional nurses for ER",
            "department": "HR"
        },
        {
            "id": 3,
            "title": "Staff HIPAA training incomplete",
            "priority": "Medium",
            "status": "Open",
            "due_date": "2024-05-20",
            "action": "Complete training for 5% remaining staff",
            "department": "Compliance"
        },
        {
            "id": 4,
            "title": "One medication error reported",
            "priority": "Medium",
            "status": "Open",
            "due_date": "2024-05-22",
            "action": "Conduct root cause analysis and staff retraining",
            "department": "Quality"
        }
    ],
    
    # ════════════════════════════════════════
    # KEY HIGHLIGHTS & ALERTS
    # ════════════════════════════════════════
    "highlights": {
        "positive": [
            "Zero post-operative infections (excellent!)",
            "100% surgical success rate",
            "Patient satisfaction stable at 4.3/5",
            "HIPAA compliance at 95%"
        ],
        "concerns": [
            "Emergency department wait time: 35 min (target: 30 min)",
            "Wheelchair availability: 8 units (low stock)",
            "1 medication error reported (resolved)",
            "ICU occupancy: 91% (near capacity)"
        ],
        "opportunities": [
            "OPD efficiency can be improved (rating 4.0)",
            "Implement faster lab testing (currently 2.5 hours)"
        ]
    }
}


def get_weekly_report() -> dict:
    """Return complete weekly report data."""
    return WEEKLY_REPORT_DATA


def get_report_metrics_only() -> dict:
    """Return only hospital metrics (lightweight)."""
    return {
        "report_week": WEEKLY_REPORT_DATA["report_week"],
        "hospital_metrics": WEEKLY_REPORT_DATA["hospital_metrics"],
        "department_stats": WEEKLY_REPORT_DATA["department_stats"]
    }


def get_clinical_data_only() -> dict:
    """Return only clinical data."""
    return {
        "report_week": WEEKLY_REPORT_DATA["report_week"],
        "clinical_summary": WEEKLY_REPORT_DATA["clinical_summary"]
    }


def get_safety_compliance_only() -> dict:
    """Return only safety & compliance data."""
    return {
        "report_week": WEEKLY_REPORT_DATA["report_week"],
        "safety_compliance": WEEKLY_REPORT_DATA["safety_compliance"]
    }

# Made with Bob
