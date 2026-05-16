"""
Test script for appointment status functionality
"""
from database.connection import SessionLocal
from services.doctor_service import DoctorService
from crud.appointment import appointment as appt_crud

def test_appointment_status():
    """Test appointment status toggle and update"""
    db = SessionLocal()
    
    try:
        # Get first appointment
        appointments = appt_crud.get_all(db)
        if not appointments:
            print("No appointments found in database")
            return
        
        test_appt = appointments[0]
        print(f"\n=== Testing Appointment Status Functionality ===")
        print(f"Appointment ID: {test_appt.id}")
        print(f"Patient: {test_appt.patient.name if test_appt.patient else 'N/A'}")
        print(f"Initial Status: {test_appt.status}")
        
        # Test toggle completion
        print("\n--- Testing Toggle Completion ---")
        result = DoctorService.toggle_appointment_completion(db, test_appt.id)
        print(f"Result: {result}")
        
        # Refresh to see changes
        db.refresh(test_appt)
        print(f"New Status: {test_appt.status}")
        
        # Toggle back
        print("\n--- Toggling Back ---")
        result = DoctorService.toggle_appointment_completion(db, test_appt.id)
        print(f"Result: {result}")
        
        db.refresh(test_appt)
        print(f"Final Status: {test_appt.status}")
        
        # Test update status
        print("\n--- Testing Update Status ---")
        result = DoctorService.update_appointment_status(db, test_appt.id, "In Progress")
        print(f"Result: {result}")
        
        db.refresh(test_appt)
        print(f"Status after update: {test_appt.status}")
        
        # Test dashboard sorting
        print("\n--- Testing Dashboard Sorting ---")
        dashboard = DoctorService.get_doctor_dashboard(db)
        if "today_appointments" in dashboard:
            print(f"Today's appointments (sorted by time):")
            for appt in dashboard["today_appointments"]:
                print(f"  - {appt['time']}: {appt['patient']} ({appt['status']})")
        
        print("\n=== All Tests Completed Successfully ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_appointment_status()

# Made with Bob
