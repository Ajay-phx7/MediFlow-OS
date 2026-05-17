"""
Mock medicine inventory for the Pharmacy admin dashboard.
"""

from datetime import date, timedelta


MEDICINE_INVENTORY = [
    {
        "id": 1,
        "name": "Paracetamol 500mg",
        "category": "Analgesic",
        "stock": 420,
        "unit": "tablets",
        "reorder_level": 120,
        "expiry_date": (date.today() + timedelta(days=210)).isoformat(),
        "status": "In stock",
    },
    {
        "id": 2,
        "name": "Amoxicillin 250mg",
        "category": "Antibiotic",
        "stock": 96,
        "unit": "capsules",
        "reorder_level": 100,
        "expiry_date": (date.today() + timedelta(days=160)).isoformat(),
        "status": "Low stock",
    },
    {
        "id": 3,
        "name": "Omeprazole 20mg",
        "category": "Gastrointestinal",
        "stock": 260,
        "unit": "capsules",
        "reorder_level": 80,
        "expiry_date": (date.today() + timedelta(days=300)).isoformat(),
        "status": "In stock",
    },
    {
        "id": 4,
        "name": "Cetirizine 10mg",
        "category": "Antihistamine",
        "stock": 180,
        "unit": "tablets",
        "reorder_level": 90,
        "expiry_date": (date.today() + timedelta(days=140)).isoformat(),
        "status": "In stock",
    },
    {
        "id": 5,
        "name": "Metformin 500mg",
        "category": "Antidiabetic",
        "stock": 75,
        "unit": "tablets",
        "reorder_level": 100,
        "expiry_date": (date.today() + timedelta(days=90)).isoformat(),
        "status": "Reorder soon",
    },
    {
        "id": 6,
        "name": "Salbutamol Inhaler",
        "category": "Respiratory",
        "stock": 34,
        "unit": "inhalers",
        "reorder_level": 25,
        "expiry_date": (date.today() + timedelta(days=240)).isoformat(),
        "status": "In stock",
    },
    {
        "id": 7,
        "name": "Ibuprofen 400mg",
        "category": "NSAID",
        "stock": 310,
        "unit": "tablets",
        "reorder_level": 100,
        "expiry_date": (date.today() + timedelta(days=180)).isoformat(),
        "status": "In stock",
    },
    {
        "id": 8,
        "name": "Atorvastatin 10mg",
        "category": "Lipid-lowering",
        "stock": 48,
        "unit": "tablets",
        "reorder_level": 60,
        "expiry_date": (date.today() + timedelta(days=75)).isoformat(),
        "status": "Low stock",
    },
]
