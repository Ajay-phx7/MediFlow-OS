from fastapi import APIRouter

from mock_data.departments import DEPARTMENTS
from mock_data.queue import QUEUE

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
    return {
        "dates": [
            "2026-05-15",
            "2026-05-16",
            "2026-05-17",
            "2026-05-18",
            "2026-05-19",
            "2026-05-20",
            "2026-05-21",
        ],
        "predicted": [98, 115, 132, 89, 142, 160, 104],
        "threshold": 120,
    }


@router.get("/live-map")
def get_live_map():
    return {"departments": DEPARTMENTS}
