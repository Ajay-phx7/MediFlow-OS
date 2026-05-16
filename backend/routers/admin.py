from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mock_data.departments import DEPARTMENTS
from mock_data.queue import QUEUE

router = APIRouter()


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    return AdminService.get_admin_stats(db)


@router.get("/queue")
def get_queue(db: Session = Depends(get_db)):
    return AdminService.get_queue(db)


@router.get("/surge-forecast")
def get_surge_forecast():
    return AdminService.get_surge_forecast()


@router.get("/live-map")
def get_live_map():
    return {"departments": DEPARTMENTS}
