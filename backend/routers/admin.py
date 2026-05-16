from fastapi import APIRouter
from pydantic import BaseModel

from mock_data.departments import DEPARTMENTS
from mock_data.queue import QUEUE
from mock_data.emergency import ALERTS, RESOURCES, PROTOCOLS
from mock_data.weekly_report import (
    get_weekly_report,
    get_report_metrics_only,
    get_clinical_data_only,
    get_safety_compliance_only
)
from ml.surge_model import generate_forecast

router = APIRouter()


@router.get("/stats")
def get_admin_stats():
    return {
        "total_patients_today": 142,
        "avg_wait_time_min": 24,
        "beds_available": 38,
        "departments_on_alert": 2,
    }


@router.get("/queue")
def get_queue():
    return {"queue": QUEUE}


@router.get("/surge-forecast")
def get_surge_forecast():
    """Get 7-day surge forecast using Prophet model."""
    try:
        forecast = generate_forecast(7)
        # Validate response structure
        required_keys = ["dates", "predicted", "upper", "lower", "threshold", "model_info"]
        if not all(key in forecast for key in required_keys):
            raise ValueError("Invalid forecast structure")
        return forecast
    except Exception as e:
        print(f"Error in surge forecast endpoint: {e}")
        import traceback
        traceback.print_exc()
        # Return fallback data for graceful degradation
        from datetime import datetime, timedelta
        today = datetime.now()
        dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        return {
            "dates": dates,
            "predicted": [120] * 7,
            "upper": [140] * 7,
            "lower": [100] * 7,
            "threshold": 120,
            "model_info": {
                "model_type": "Fallback",
                "training_days": 0,
                "last_trained": today.strftime("%Y-%m-%d"),
                "seasonality": [],
                "accuracy_mape": 0.0
            }
        }


class SurgeForecastRequest(BaseModel):
    days: int = 14


@router.post("/surge-forecast/custom")
def get_surge_forecast_custom(request: SurgeForecastRequest):
    """Get custom-length surge forecast using Prophet model."""
    try:
        # Clamp days to valid range (1-365)
        days = max(1, min(365, request.days))
        forecast = generate_forecast(days)
        # Validate response structure
        required_keys = ["dates", "predicted", "upper", "lower", "threshold", "model_info"]
        if not all(key in forecast for key in required_keys):
            raise ValueError("Invalid forecast structure")
        return forecast
    except Exception as e:
        print(f"Error in custom surge forecast endpoint: {e}")
        import traceback
        traceback.print_exc()
        # Return fallback data for graceful degradation
        from datetime import datetime, timedelta
        today = datetime.now()
        days = max(1, min(365, request.days))
        dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        return {
            "dates": dates,
            "predicted": [120] * days,
            "upper": [140] * days,
            "lower": [100] * days,
            "threshold": 120,
            "model_info": {
                "model_type": "Fallback",
                "training_days": 0,
                "last_trained": today.strftime("%Y-%m-%d"),
                "seasonality": [],
                "accuracy_mape": 0.0
            }
        }


@router.get("/live-map")
def get_live_map():
    return {"departments": DEPARTMENTS}


# Emergency endpoints
@router.get("/emergency/alerts")
def get_emergency_alerts():
    return ALERTS


@router.get("/emergency/resources")
def get_emergency_resources():
    return RESOURCES


class EscalateRequest(BaseModel):
    alertId: str
    level: str


@router.post("/emergency/escalate")
def escalate_alert(request: EscalateRequest):
    return {
        "success": True,
        "alertId": request.alertId,
        "message": "Alert escalated successfully",
    }


@router.get("/emergency/protocol")
def get_emergency_protocol(type: str = "Cardiac Arrest"):
    protocol_steps = PROTOCOLS.get(type, PROTOCOLS["Cardiac Arrest"])
    return {"type": type, "steps": protocol_steps}


# Weekly Report endpoints
@router.get("/weekly-report")
def get_weekly_report_endpoint():
    """
    Get complete weekly report with all sections.
    
    Response includes:
    - Hospital metrics (KPIs)
    - Department statistics
    - Clinical data (surgeries, diagnoses, labs)
    - Resource utilization
    - Safety & compliance
    - Daily trends
    - Action items
    - Highlights & alerts
    
    Returns: Complete WEEKLY_REPORT_DATA dict
    """
    return get_weekly_report()


@router.get("/weekly-report/metrics")
def get_report_metrics():
    """
    Get ONLY hospital metrics section (lightweight).
    
    Useful for: Dashboard widget preview
    
    Response:
    {
        "report_week": "May 12-18, 2024",
        "hospital_metrics": { ... },
        "department_stats": [ ... ]
    }
    """
    return get_report_metrics_only()


@router.get("/weekly-report/clinical")
def get_report_clinical():
    """
    Get ONLY clinical data section.
    
    Includes:
    - Surgery statistics
    - Top diagnoses
    - Lab tests
    - Medication usage
    
    Response:
    {
        "report_week": "May 12-18, 2024",
        "clinical_summary": { ... }
    }
    """
    return get_clinical_data_only()


@router.get("/weekly-report/compliance")
def get_report_compliance():
    """
    Get ONLY safety & compliance data section.
    
    Includes:
    - Incidents (falls, medication errors, etc)
    - Data security (HIPAA, breaches)
    - Infection control
    - Quality metrics
    - Regulatory status
    
    Response:
    {
        "report_week": "May 12-18, 2024",
        "safety_compliance": { ... }
    }
    """
    return get_safety_compliance_only()
