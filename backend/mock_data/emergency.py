ALERTS = [
    {
        "id": "ALT-001",
        "type": "Cardiac Arrest",
        "location": "ER Bay 3",
        "severity": "Critical",
        "elapsed": "4 min ago",
        "escalated": False,
    },
    {
        "id": "ALT-002",
        "type": "Mass Casualty Incoming",
        "location": "Ambulance Bay",
        "severity": "High",
        "elapsed": "2 min ago",
        "escalated": False,
        "note": "3 patients ETA 8 min",
    },
    {
        "id": "ALT-003",
        "type": "ICU Bed Shortage",
        "location": "ICU Wing B",
        "severity": "Moderate",
        "elapsed": "19 min ago",
        "escalated": False,
    },
]

RESOURCES = {
    "ambulances": [
        {"id": "AMB-1", "status": "available"},
        {"id": "AMB-2", "status": "en-route"},
        {"id": "AMB-3", "status": "available"},
        {"id": "AMB-4", "status": "en-route"},
        {"id": "AMB-5", "status": "available"},
        {"id": "AMB-6", "status": "maintenance"},
    ],
    "er_beds": {"free": 4, "total": 12},
    "on_call_surgeons": 2,
    "blood_bank": [
        {"type": "O-", "status": "low"},
        {"type": "A+", "status": "adequate"},
        {"type": "B+", "status": "adequate"},
        {"type": "AB+", "status": "low"},
    ],
}

PROTOCOLS = {
    "Cardiac Arrest": [
        "Call code blue immediately",
        "Assign resuscitation team to bay",
        "Prepare defibrillator and crash cart",
        "Notify on-call cardiologist",
        "Clear corridor to ER",
        "Document time of arrest",
    ],
    "Trauma": [
        "Activate trauma team",
        "Prepare trauma bay",
        "Alert radiology for fast-track CT",
        "Cross-match blood type",
        "Notify surgical team on standby",
        "Assign dedicated trauma nurse",
    ],
    "Fire": [
        "Trigger fire alarm",
        "Evacuate non-ambulatory patients first",
        "Notify fire department (call 101)",
        "Shut down HVAC in affected zone",
        "Account for all staff and patients",
        "Move critical patients to safe zone",
    ],
    "Mass Casualty": [
        "Activate MCI protocol",
        "Set up triage area at ambulance bay",
        "Call in off-duty emergency staff",
        "Clear OPD for overflow patients",
        "Coordinate with blood bank for reserves",
        "Assign media liaison officer",
    ],
}

# Made with Bob
