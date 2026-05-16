# Appointment Status Management Implementation

## Summary of Changes

This implementation adds comprehensive appointment status management functionality to the doctor dashboard, including the ability to toggle appointment completion and sort patients by their upcoming appointment times.

## Features Implemented

### 1. Toggle Appointment Completion
- **Functionality**: Doctors can toggle an appointment's completion status with a single action
- **Behavior**:
  - If status is "Completed" → changes to "Scheduled"
  - If status is anything else (Scheduled, In Progress, etc.) → changes to "Completed"
- **Auto-updates**: The `updated_at` timestamp is automatically updated

### 2. Manual Status Updates
- **Functionality**: Doctors can manually set appointment status to any valid state
- **Valid Statuses**:
  - Scheduled
  - In Progress
  - Completed
  - Cancelled
- **Validation**: Invalid status values are rejected with an error message

### 3. Sorted Patient Queues
- **Today's Appointments**: Sorted by scheduled time (earliest first)
- **Assigned Patients List**: Sorted by upcoming appointment time
  - Patients with upcoming appointments appear first, ordered by appointment time
  - Patients without upcoming appointments appear last
- **Next Patient**: Automatically determined from pending appointments in chronological order

## API Endpoints

### 1. Toggle Appointment Completion
```
POST /api/doctor/appointment/{appointment_id}/toggle-completion
```

**Response Example:**
```json
{
  "success": true,
  "appointment": {
    "id": 1,
    "patient_id": 5,
    "patient_name": "John Doe",
    "doctor_id": 2,
    "doctor_name": "Dr. Smith",
    "scheduled_time": "2026-05-16T10:30:00",
    "status": "Completed",
    "complaint": "Chest pain",
    "notes": "Patient reports improvement",
    "created_at": "2026-05-15T08:00:00",
    "updated_at": "2026-05-16T14:00:00"
  },
  "message": "Appointment status changed to Completed"
}
```

### 2. Update Appointment Status
```
PUT /api/doctor/appointment/{appointment_id}/status
Content-Type: application/json

{
  "status": "In Progress"
}
```

**Response Example:**
```json
{
  "success": true,
  "appointment": {
    "id": 1,
    "status": "In Progress",
    ...
  },
  "message": "Appointment status updated to In Progress"
}
```

## Code Changes

### 1. CRUD Layer (`backend/crud/appointment.py`)

#### New Methods:
```python
def update_status(self, db: Session, appointment_id: int, status: str) -> Appointment:
    """Update appointment status"""
    appointment = self.get(db, appointment_id)
    if appointment:
        appointment.status = status
        appointment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(appointment)
    return appointment

def toggle_completion(self, db: Session, appointment_id: int) -> Appointment:
    """Toggle appointment between Completed and Scheduled/In Progress status"""
    appointment = self.get(db, appointment_id)
    if appointment:
        if appointment.status == "Completed":
            appointment.status = "Scheduled"
        else:
            appointment.status = "Completed"
        appointment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(appointment)
    return appointment
```

### 2. Service Layer (`backend/services/doctor_service.py`)

#### New Service Methods:
```python
@staticmethod
def toggle_appointment_completion(db: Session, appointment_id: int):
    """Toggle appointment completion status"""
    appointment = appt_crud.toggle_completion(db, appointment_id)
    if not appointment:
        return {"error": "Appointment not found"}
    return {
        "success": True,
        "appointment": appointment.to_dict(),
        "message": f"Appointment status changed to {appointment.status}"
    }

@staticmethod
def update_appointment_status(db: Session, appointment_id: int, status: str):
    """Update appointment status with validation"""
    valid_statuses = ["Scheduled", "In Progress", "Completed", "Cancelled"]
    if status not in valid_statuses:
        return {
            "error": "Invalid status",
            "message": f"Status must be one of: {', '.join(valid_statuses)}"
        }
    appointment = appt_crud.update_status(db, appointment_id, status)
    if not appointment:
        return {"error": "Appointment not found"}
    return {
        "success": True,
        "appointment": appointment.to_dict(),
        "message": f"Appointment status updated to {status}"
    }
```

#### Updated Methods:

**`get_doctor_dashboard()`**:
- Sorts today's appointments by scheduled time (earliest first)
- Determines next patient from sorted pending appointments
- Returns appointments in chronological order

**`_build_patient_summary()`**:
- Sorts patients by their upcoming appointment time
- Patients with appointments appear first, ordered by time
- Patients without appointments appear last

**`get_all_patients()`**:
- Applies same sorting logic as `_build_patient_summary()`
- Ensures consistent ordering across all patient lists

### 3. Router Layer (`backend/routers/doctor.py`)

#### New Model:
```python
class AppointmentStatusUpdate(BaseModel):
    status: str
```

#### New Endpoints:
```python
@router.post("/appointment/{appointment_id}/toggle-completion")
def toggle_appointment_completion(appointment_id: int, db: Session = Depends(get_db)):
    """Toggle appointment completion status"""
    return DoctorService.toggle_appointment_completion(db, appointment_id)

@router.put("/appointment/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update appointment status"""
    return DoctorService.update_appointment_status(db, appointment_id, payload.status)
```

## Dashboard Response Structure

The doctor dashboard now returns data with sorted appointments:

```json
{
  "doctor": {...},
  "appointments_today": 5,
  "completed": 2,
  "pending": 3,
  "today_appointments": [
    {
      "id": 1,
      "time": "09:00 AM",
      "date": "2026-05-16",
      "status": "Completed",
      "patient": "John Doe",
      "reason": "Checkup"
    },
    {
      "id": 2,
      "time": "10:30 AM",
      "date": "2026-05-16",
      "status": "In Progress",
      "patient": "Jane Smith",
      "reason": "Follow-up"
    },
    {
      "id": 3,
      "time": "02:00 PM",
      "date": "2026-05-16",
      "status": "Scheduled",
      "patient": "Bob Johnson",
      "reason": "Consultation"
    }
  ],
  "next_patient": {
    "name": "Jane Smith",
    "age": 45,
    "complaint": "Follow-up"
  },
  "assigned_patients": [
    // Sorted by upcoming appointment time
  ]
}
```

## Frontend Integration Examples

### Toggle Completion Button
```javascript
async function toggleAppointmentCompletion(appointmentId) {
  const response = await fetch(
    `/api/doctor/appointment/${appointmentId}/toggle-completion`,
    { method: 'POST' }
  );
  const result = await response.json();
  if (result.success) {
    console.log(`Status changed to: ${result.appointment.status}`);
    refreshDashboard();
  }
}
```

### Status Dropdown
```javascript
async function updateAppointmentStatus(appointmentId, newStatus) {
  const response = await fetch(
    `/api/doctor/appointment/${appointmentId}/status`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    }
  );
  const result = await response.json();
  if (result.success) {
    refreshDashboard();
  }
}
```

## Benefits

1. **Streamlined Workflow**: One-click completion toggle reduces manual steps
2. **Organized Queue**: Chronological sorting helps doctors see who's next
3. **Flexible Control**: Manual status updates for special cases
4. **Real-time Updates**: Immediate reflection of status changes
5. **Better Patient Flow**: Automatic queue management based on appointment times
6. **Consistent Ordering**: All patient lists sorted by upcoming appointments

## Testing Recommendations

1. Test toggle completion on appointments with different statuses
2. Verify sorting of today's appointments by time
3. Confirm assigned patients list is sorted by upcoming appointment
4. Test manual status updates with all valid statuses
5. Verify error handling for invalid statuses
6. Check that next patient updates correctly after status changes
7. Ensure timestamps update properly on status changes

## Notes

- All status changes automatically update the `updated_at` timestamp
- Only "Scheduled" and "In Progress" appointments are considered pending
- Completed and Cancelled appointments are excluded from the next patient queue
- Sorting ensures earliest scheduled appointments always appear first
- Type checker warnings for SQLAlchemy are expected and do not affect runtime behavior