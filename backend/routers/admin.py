from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.admin_service import AdminService

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
def get_live_map(db: Session = Depends(get_db)):
    return AdminService.get_live_map(db)

# Made with Bob
