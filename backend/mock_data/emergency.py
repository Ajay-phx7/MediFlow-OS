"""
Emergency department mock data
Provides emergency alerts and incident data
"""

from datetime import datetime, timedelta
from typing import List, Dict

# Emergency alert levels
ALERT_LEVELS = {
    "critical": {"color": "red", "priority": 1},
    "high": {"color": "orange", "priority": 2},
    "medium": {"color": "yellow", "priority": 3},
    "low": {"color": "blue", "priority": 4},
}

# Current emergency alerts
EMERGENCY_ALERTS = [
    {
        "id": "alert_001",
        "type": "surge",
        "level": "high",
        "title": "Patient Surge Detected",
        "description": "Emergency department experiencing 40% above normal patient volume",
        "department": "Emergency",
        "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
        "status": "active",
        "affected_areas": ["ER", "Triage", "Waiting Room"],
        "recommended_actions": [
            "Activate surge protocol",
            "Call in additional staff",
            "Prepare overflow areas"
        ]
    },
    {
        "id": "alert_002",
        "type": "capacity",
        "level": "critical",
        "title": "ICU Capacity Critical",
        "description": "ICU at 95% capacity with 2 beds remaining",
        "department": "ICU",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "status": "active",
        "affected_areas": ["ICU", "Critical Care"],
        "recommended_actions": [
            "Prepare for patient transfers",
            "Contact nearby hospitals",
            "Expedite discharge reviews"
        ]
    },
    {
        "id": "alert_003",
        "type": "staffing",
        "level": "medium",
        "title": "Staffing Shortage - Night Shift",
        "description": "3 nurses called in sick for tonight's shift",
        "department": "Nursing",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "status": "active",
        "affected_areas": ["Medical Ward", "Surgical Ward"],
        "recommended_actions": [
            "Contact on-call staff",
            "Redistribute patient assignments",
            "Consider temporary agency staff"
        ]
    },
    {
        "id": "alert_004",
        "type": "equipment",
        "level": "low",
        "title": "Equipment Maintenance Scheduled",
        "description": "MRI machine scheduled for maintenance tomorrow",
        "department": "Radiology",
        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
        "status": "scheduled",
        "affected_areas": ["Radiology", "Imaging"],
        "recommended_actions": [
            "Reschedule non-urgent scans",
            "Inform referring physicians",
            "Update appointment system"
        ]
    }
]

# Emergency incidents history
EMERGENCY_INCIDENTS = [
    {
        "id": "incident_001",
        "date": "2026-05-15",
        "type": "mass_casualty",
        "severity": "high",
        "description": "Multi-vehicle accident on highway",
        "patients_affected": 12,
        "response_time_minutes": 8,
        "resolution_time_hours": 6,
        "status": "resolved"
    },
    {
        "id": "incident_002",
        "date": "2026-05-14",
        "type": "system_failure",
        "severity": "medium",
        "description": "Electronic health records system outage",
        "patients_affected": 0,
        "response_time_minutes": 15,
        "resolution_time_hours": 2,
        "status": "resolved"
    },
    {
        "id": "incident_003",
        "date": "2026-05-13",
        "type": "surge",
        "severity": "medium",
        "description": "Flu outbreak in local school",
        "patients_affected": 28,
        "response_time_minutes": 30,
        "resolution_time_hours": 12,
        "status": "resolved"
    }
]

# Emergency response protocols
EMERGENCY_PROTOCOLS = {
    "surge": {
        "name": "Patient Surge Protocol",
        "steps": [
            "Activate command center",
            "Notify all department heads",
            "Call in additional staff",
            "Prepare overflow areas",
            "Implement fast-track triage",
            "Coordinate with nearby facilities"
        ],
        "estimated_activation_time": "15 minutes"
    },
    "mass_casualty": {
        "name": "Mass Casualty Incident Protocol",
        "steps": [
            "Activate emergency operations center",
            "Implement incident command system",
            "Clear emergency department",
            "Set up triage areas",
            "Mobilize trauma teams",
            "Coordinate with EMS and law enforcement"
        ],
        "estimated_activation_time": "10 minutes"
    },
    "evacuation": {
        "name": "Hospital Evacuation Protocol",
        "steps": [
            "Sound evacuation alarm",
            "Notify all staff and patients",
            "Prioritize patient movement",
            "Coordinate with emergency services",
            "Establish alternative care sites",
            "Account for all patients and staff"
        ],
        "estimated_activation_time": "5 minutes"
    }
}

# Emergency contact information
EMERGENCY_CONTACTS = [
    {
        "role": "Emergency Director",
        "name": "Dr. Sarah Mitchell",
        "phone": "+1-555-0101",
        "email": "s.mitchell@mediflow.hospital",
        "availability": "24/7"
    },
    {
        "role": "Nursing Supervisor",
        "name": "Jennifer Adams",
        "phone": "+1-555-0102",
        "email": "j.adams@mediflow.hospital",
        "availability": "24/7"
    },
    {
        "role": "Security Chief",
        "name": "Michael Torres",
        "phone": "+1-555-0103",
        "email": "m.torres@mediflow.hospital",
        "availability": "24/7"
    },
    {
        "role": "Facilities Manager",
        "name": "Robert Chen",
        "phone": "+1-555-0104",
        "email": "r.chen@mediflow.hospital",
        "availability": "On-call"
    }
]


def get_active_alerts() -> List[Dict]:
    """Get all active emergency alerts"""
    return [alert for alert in EMERGENCY_ALERTS if alert["status"] == "active"]


def get_alerts_by_level(level: str) -> List[Dict]:
    """Get alerts filtered by severity level"""
    return [alert for alert in EMERGENCY_ALERTS if alert["level"] == level]


def get_critical_alerts() -> List[Dict]:
    """Get only critical alerts"""
    return get_alerts_by_level("critical")


def get_recent_incidents(days: int = 7) -> List[Dict]:
    """Get emergency incidents from the last N days"""
    cutoff_date = datetime.now() - timedelta(days=days)
    return [
        incident for incident in EMERGENCY_INCIDENTS
        if datetime.fromisoformat(incident["date"]) >= cutoff_date
    ]


def get_protocol(protocol_type: str) -> Dict:
    """Get emergency protocol by type"""
    return EMERGENCY_PROTOCOLS.get(protocol_type, {})


def get_emergency_contacts() -> List[Dict]:
    """Get all emergency contact information"""
    return EMERGENCY_CONTACTS

# Made with Bob
