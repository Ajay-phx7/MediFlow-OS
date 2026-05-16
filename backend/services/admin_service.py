from sqlalchemy.orm import Session
from crud import department as dept_crud, queue as queue_crud
from database.models import Department, QueueEntry


class AdminService:
    @staticmethod
    def get_admin_stats(db: Session):
        """Get admin dashboard statistics"""
        total_patients = sum(dept.current_patients for dept in dept_crud.get_all(db))
        queue_entries = queue_crud.get_waiting(db)
        avg_wait = sum(q.wait_time_minutes for q in queue_entries) / len(queue_entries) if queue_entries else 0
        high_congestion_depts = dept_crud.get_high_congestion(db)
        
        return {
            "total_patients_today": total_patients,
            "avg_wait_time_min": int(avg_wait),
            "beds_available": 38,  # This could be calculated from department capacity
            "departments_on_alert": len(high_congestion_depts),
        }

    @staticmethod
    def get_queue(db: Session):
        """Get all queue entries"""
        queue_entries = queue_crud.get_waiting(db)
        return {"queue": [q.to_dict() for q in queue_entries]}

    @staticmethod
    def get_surge_forecast():
        """Get surge prediction forecast (mock data for now)"""
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

    @staticmethod
    def get_live_map(db: Session):
        """Get live department map with congestion data"""
        departments = dept_crud.get_all(db)
        return {"departments": [dept.to_dict() for dept in departments]}


# Made with Bob
