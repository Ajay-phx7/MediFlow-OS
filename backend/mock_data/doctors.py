DOCTORS = [
    {"name": "Dr. Sneha Rao", "department": "Cardiology"},
    {"name": "Dr. Arjun Patel", "department": "Orthopaedics"},
    {"name": "Dr. Fatima Shaikh", "department": "Paediatrics"},
    {"name": "Dr. Vikram Nair", "department": "Emergency"},
]

DOCTOR_DASHBOARD = {
    "appointments_today": 8,
    "completed": 3,
    "pending": 5,
    "next_patient": {
        "name": "Ravi Kumar",
        "age": 35,
        "complaint": "Chest discomfort and fatigue",
    },
}

DOCTOR_PATIENTS = [
    {
        "name": "Ravi Kumar",
        "age": 35,
        "time": "10:30 AM",
        "status": "In Consultation",
        "history": "Hypertension, elevated LDL, previous ECG normal.",
    },
    {
        "name": "Aisha Khan",
        "age": 28,
        "time": "11:15 AM",
        "status": "Waiting",
        "history": "Allergic rhinitis, mild asthma, no chronic meds.",
    },
    {
        "name": "Priya Mehta",
        "age": 42,
        "time": "12:00 PM",
        "status": "Done",
        "history": "Post-op review for knee arthroscopy, pain improving.",
    },
]

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
