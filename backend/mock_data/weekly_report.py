"""
Weekly report mock data
Provides hospital performance metrics and analytics
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Current week date range
current_date = datetime.now()
week_start = current_date - timedelta(days=current_date.weekday())
week_end = week_start + timedelta(days=6)

WEEKLY_REPORT = {
    "report_id": "WR_2026_W20",
    "week_start": week_start.strftime("%Y-%m-%d"),
    "week_end": week_end.strftime("%Y-%m-%d"),
    "generated_at": datetime.now().isoformat(),
    
    # Overall metrics
    "summary": {
        "total_patients": 1247,
        "total_admissions": 342,
        "total_discharges": 328,
        "average_length_of_stay_days": 4.2,
        "bed_occupancy_rate": 87.5,
        "emergency_visits": 456,
        "outpatient_visits": 791
    },
    
    # Daily breakdown
    "daily_metrics": [
        {
            "date": (week_start + timedelta(days=0)).strftime("%Y-%m-%d"),
            "day": "Monday",
            "patients": 198,
            "admissions": 52,
            "discharges": 48,
            "emergency_visits": 72,
            "bed_occupancy": 89.2
        },
        {
            "date": (week_start + timedelta(days=1)).strftime("%Y-%m-%d"),
            "day": "Tuesday",
            "patients": 185,
            "admissions": 49,
            "discharges": 51,
            "emergency_visits": 68,
            "bed_occupancy": 87.8
        },
        {
            "date": (week_start + timedelta(days=2)).strftime("%Y-%m-%d"),
            "day": "Wednesday",
            "patients": 192,
            "admissions": 54,
            "discharges": 47,
            "emergency_visits": 71,
            "bed_occupancy": 88.5
        },
        {
            "date": (week_start + timedelta(days=3)).strftime("%Y-%m-%d"),
            "day": "Thursday",
            "patients": 178,
            "admissions": 46,
            "discharges": 49,
            "emergency_visits": 65,
            "bed_occupancy": 86.3
        },
        {
            "date": (week_start + timedelta(days=4)).strftime("%Y-%m-%d"),
            "day": "Friday",
            "patients": 189,
            "admissions": 51,
            "discharges": 53,
            "emergency_visits": 69,
            "bed_occupancy": 85.9
        },
        {
            "date": (week_start + timedelta(days=5)).strftime("%Y-%m-%d"),
            "day": "Saturday",
            "patients": 152,
            "admissions": 45,
            "discharges": 42,
            "emergency_visits": 58,
            "bed_occupancy": 84.7
        },
        {
            "date": (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            "day": "Sunday",
            "patients": 153,
            "admissions": 45,
            "discharges": 38,
            "emergency_visits": 53,
            "bed_occupancy": 87.1
        }
    ],
    
    # Department performance
    "department_metrics": [
        {
            "department": "Emergency",
            "patients_seen": 456,
            "average_wait_time_minutes": 28,
            "patient_satisfaction": 4.2,
            "staff_utilization": 92.3,
            "trend": "up"
        },
        {
            "department": "Cardiology",
            "patients_seen": 187,
            "average_wait_time_minutes": 15,
            "patient_satisfaction": 4.6,
            "staff_utilization": 85.7,
            "trend": "stable"
        },
        {
            "department": "Orthopedics",
            "patients_seen": 142,
            "average_wait_time_minutes": 22,
            "patient_satisfaction": 4.4,
            "staff_utilization": 88.2,
            "trend": "up"
        },
        {
            "department": "Pediatrics",
            "patients_seen": 203,
            "average_wait_time_minutes": 18,
            "patient_satisfaction": 4.7,
            "staff_utilization": 79.5,
            "trend": "down"
        },
        {
            "department": "Surgery",
            "patients_seen": 98,
            "average_wait_time_minutes": 12,
            "patient_satisfaction": 4.5,
            "staff_utilization": 94.1,
            "trend": "stable"
        },
        {
            "department": "ICU",
            "patients_seen": 67,
            "average_wait_time_minutes": 0,
            "patient_satisfaction": 4.3,
            "staff_utilization": 96.8,
            "trend": "up"
        }
    ],
    
    # Quality metrics
    "quality_metrics": {
        "patient_satisfaction_score": 4.4,
        "readmission_rate": 8.2,
        "mortality_rate": 1.1,
        "infection_rate": 0.8,
        "medication_error_rate": 0.3,
        "fall_rate": 1.2
    },
    
    # Financial metrics
    "financial_metrics": {
        "total_revenue": 2847500,
        "total_expenses": 2156300,
        "net_income": 691200,
        "revenue_per_patient": 2284,
        "cost_per_patient": 1729,
        "profit_margin": 24.3
    },
    
    # Staffing metrics
    "staffing_metrics": {
        "total_staff": 487,
        "nurses": 245,
        "doctors": 89,
        "support_staff": 153,
        "overtime_hours": 342,
        "sick_leave_hours": 156,
        "vacancy_rate": 4.2,
        "turnover_rate": 8.7
    },
    
    # Key highlights
    "highlights": [
        {
            "type": "achievement",
            "title": "Record Patient Satisfaction",
            "description": "Achieved highest patient satisfaction score of 4.7 in Pediatrics department",
            "impact": "positive"
        },
        {
            "type": "concern",
            "title": "ICU Capacity Strain",
            "description": "ICU operating at 96.8% capacity, approaching critical threshold",
            "impact": "negative"
        },
        {
            "type": "improvement",
            "title": "Reduced Wait Times",
            "description": "Emergency department wait times decreased by 12% compared to last week",
            "impact": "positive"
        },
        {
            "type": "alert",
            "title": "Staffing Shortage",
            "description": "Nursing vacancy rate increased to 4.2%, recruitment efforts needed",
            "impact": "negative"
        }
    ],
    
    # Recommendations
    "recommendations": [
        {
            "priority": "high",
            "category": "capacity",
            "recommendation": "Increase ICU capacity or implement patient transfer protocols",
            "expected_impact": "Reduce ICU strain and improve patient outcomes"
        },
        {
            "priority": "high",
            "category": "staffing",
            "recommendation": "Accelerate nursing recruitment and consider temporary staffing",
            "expected_impact": "Reduce staff burnout and maintain quality of care"
        },
        {
            "priority": "medium",
            "category": "efficiency",
            "recommendation": "Implement fast-track system in Emergency department",
            "expected_impact": "Further reduce wait times and improve patient flow"
        },
        {
            "priority": "medium",
            "category": "quality",
            "recommendation": "Review readmission cases to identify preventable factors",
            "expected_impact": "Reduce readmission rate and improve patient outcomes"
        },
        {
            "priority": "low",
            "category": "financial",
            "recommendation": "Optimize supply chain management to reduce costs",
            "expected_impact": "Improve profit margins without affecting quality"
        }
    ],
    
    # Comparison with previous week
    "week_over_week_change": {
        "total_patients": 3.2,
        "admissions": 5.1,
        "discharges": 2.8,
        "emergency_visits": -2.4,
        "bed_occupancy": 1.7,
        "patient_satisfaction": 0.2,
        "average_wait_time": -12.0
    }
}


def get_weekly_report() -> Dict:
    """Get the current weekly report"""
    return WEEKLY_REPORT


def get_department_summary(department: str) -> Dict:
    """Get summary for a specific department"""
    for dept in WEEKLY_REPORT["department_metrics"]:
        if dept["department"].lower() == department.lower():
            return dept
    return {}


def get_quality_metrics() -> Dict:
    """Get quality metrics"""
    return WEEKLY_REPORT["quality_metrics"]


def get_financial_summary() -> Dict:
    """Get financial summary"""
    return WEEKLY_REPORT["financial_metrics"]


def get_staffing_summary() -> Dict:
    """Get staffing summary"""
    return WEEKLY_REPORT["staffing_metrics"]


def get_highlights() -> List[Dict]:
    """Get key highlights"""
    return WEEKLY_REPORT["highlights"]


def get_recommendations(priority: Optional[str] = None) -> List[Dict]:
    """Get recommendations, optionally filtered by priority"""
    recommendations = WEEKLY_REPORT["recommendations"]
    if priority:
        return [r for r in recommendations if r["priority"] == priority]
    return recommendations


def get_daily_metrics(date: Optional[str] = None) -> Dict:
    """Get metrics for a specific date"""
    if date:
        for day in WEEKLY_REPORT["daily_metrics"]:
            if day["date"] == date:
                return day
    return {}


def get_report_metrics_only() -> Dict:
    """Get only the summary metrics from the report"""
    return WEEKLY_REPORT["summary"]


def get_clinical_data_only() -> Dict:
    """Get only clinical quality metrics"""
    return {
        "quality_metrics": WEEKLY_REPORT["quality_metrics"],
        "department_metrics": WEEKLY_REPORT["department_metrics"]
    }


def get_safety_compliance_only() -> Dict:
    """Get only safety and compliance metrics"""
    return {
        "infection_rate": WEEKLY_REPORT["quality_metrics"]["infection_rate"],
        "medication_error_rate": WEEKLY_REPORT["quality_metrics"]["medication_error_rate"],
        "fall_rate": WEEKLY_REPORT["quality_metrics"]["fall_rate"],
        "mortality_rate": WEEKLY_REPORT["quality_metrics"]["mortality_rate"]
    }


def get_trend_data() -> Dict:
    """Get week-over-week trend data"""
    return WEEKLY_REPORT["week_over_week_change"]

# Made with Bob
