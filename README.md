# MediFlow OS

MediFlow OS is a full-stack hospital management platform with role-based dashboards, appointment workflows, live department monitoring, and an AI-powered medical scribe.

## Overview

The app is organized around three user roles:

- Admin / Reception: operational dashboard, queue tracking, surge forecasting, department chat, and emergency monitoring.
- Doctor: patient roster, appointment management, and AI scribe tools for consultation documentation.
- Patient: dashboard, doctor browsing, slot lookup, appointment booking, and health reports.

Authentication is selection-based rather than password-based. Users pick an account to enter the app, and the frontend stores the active role and selected user in local storage for API requests.

## Key Features

### Admin / Reception

- Dashboard summary with live operational stats.
- Queue management for waiting patients.
- Surge forecasting for upcoming demand.
- Live resource monitoring across departments.
- Department chat for coordination between teams.
- Emergency control views backed by emergency mock data.

### Doctor

- Doctor dashboard with patient and appointment context.
- Comprehensive patient list for the selected doctor.
- Appointment status updates and date-range appointment views.
- AI Scribe for generating SOAP notes and prescriptions from text or audio.
- Audio transcription via microphone streaming or uploaded files.
- Real-time transcript updates over WebSocket.

### Patient

- Patient dashboard with personal care information.
- Browse available doctors.
- Check available appointment slots.
- Book appointments.
- View health reports and appointment history.

### AI Medical Scribe

- Live microphone capture with pause and resume.
- Recording timer and local audio upload support.
- Real-time transcription over WebSocket.
- SOAP note and prescription generation from consultation transcripts.
- IBM Watson Speech-to-Text as the primary transcription path.
- Grok/Groq fallback transcription when IBM is unavailable.
- Google Gemini-based medical note generation with API key rotation and quota backoff.


## Tech Stack

- Frontend: React 18, React Router, Vite, Tailwind CSS, Lucide icons.
- Backend: FastAPI, SQLAlchemy, WebSockets.
- AI: IBM Watson Speech-to-Text, Grok/Groq fallback, Google Gemini.
- Storage: Database-backed demo data and local mock datasets.

## Project Structure

```
backend/
	main.py, config.py, requirements.txt
	routers/          # Auth, admin, doctor, patient, websocket endpoints
	services/         # Business logic, AI integration, appointment handling
	crud/             # Database access helpers
	database/         # Models and DB connection
	mock_data/        # Demo emergency and fallback datasets

frontend/
	src/
		pages/          # Admin, Doctor, Patient screens
		components/     # Shared UI components
		api/            # Axios client and endpoint wrappers
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 after both services are running.

### AI Configuration

If you want the transcription and AI generation paths to use live providers, set the required API keys in the backend environment. When keys are missing, the app falls back to mock or degraded behavior where possible.

## API Surface

### Authentication

- `GET /api/auth/admins` and `GET /api/auth/admins/{id}`
- `GET /api/auth/doctors` and `GET /api/auth/doctors/{id}`
- `GET /api/auth/patients` and `GET /api/auth/patients/{id}`

### Admin

- `GET /api/admin/stats`
- `GET /api/admin/queue`
- `GET /api/admin/surge-forecast`
- `GET /api/admin/live-map`
- `GET /api/admin/chat/all`
- `GET /api/admin/chat/{department}`
- `POST /api/admin/chat`

### Doctor

- `GET /api/doctor/dashboard`
- `GET /api/doctor/patients`
- `GET /api/doctor/patient`
- `GET /api/doctor/appointments-by-status`
- `GET /api/doctor/appointments-range`
- `PUT /api/doctor/appointment/{appointment_id}/status`
- `POST /api/doctor/appointment/{appointment_id}/toggle-completion`
- `POST /api/doctor/scribe`
- `POST /api/doctor/scribe/audio`

### Patient

- `GET /api/patient/dashboard`
- `GET /api/patient/health-report`
- `GET /api/patient/doctors`
- `GET /api/patient/available-slots`
- `POST /api/patient/book-appointment`
- `GET /api/patient/appointments`

### WebSocket

- `WS /api/ws/scribe/{client_id}` for real-time audio streaming and transcript updates.

## Notes

- The app is database-backed, but login is still a selection flow rather than a secure password system.
- AI features can run in fallback mode when live provider keys are missing.
- CORS is configured for `http://localhost:5173`.
- Microphone access requires HTTPS in production.

---

Made with Bob
