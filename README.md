# MediCore

MediCore is a full-stack MVP Hospital Management Platform built as a dummy prototype.
It uses hardcoded mock data only (no database, no authentication). The goal is to
show structure, routing, and UI for three roles: Admin, Doctor, and Patient.

## Tech Stack

- Frontend: React 18 + Vite + React Router v6 + Tailwind CSS
- Backend: FastAPI (Python)
- State: React useState / useContext only
- HTTP: Axios (frontend calls FastAPI endpoints)
- Charts: Recharts
- Icons: Lucide React

## Project Structure

```
backend/
	main.py
	routers/
		admin.py
		doctor.py
		patient.py
	mock_data/
		patients.py
		doctors.py
		queue.py
		departments.py
	requirements.txt

frontend/
	index.html
	vite.config.js
	tailwind.config.js
	src/
		App.jsx
		main.jsx
		api/index.js
		context/AppContext.jsx
		pages/
			Home.jsx
			admin/
			doctor/
			patient/
		components/
```

## Frontend Routes

- / -> Role selector landing page
- /admin -> Admin dashboard, queue, surge forecast, live map, dept chat
- /doctor -> Doctor dashboard, patients list, AI scribe
- /patient -> Patient dashboard, booking, live map, health report

## Backend Endpoints (Mock JSON)

All endpoints return hardcoded JSON from the mock_data module.

- GET /api/admin/stats
- GET /api/admin/queue
- GET /api/admin/surge-forecast
- GET /api/admin/live-map
- GET /api/doctor/dashboard
- GET /api/doctor/patients
- POST /api/doctor/scribe
- GET /api/patient/dashboard
- GET /api/patient/health-report

## Mock Data Highlights

- Queue: Aisha Khan (T-001, Emergency), Ravi Kumar (T-002, Cardiology), Priya Mehta (T-003, OPD)
- Live map: Emergency, ICU, OPD, Cardiology, Orthopaedics, Paediatrics with congestion badges
- Surge forecast: next 7 days predicted = [98, 115, 132, 89, 142, 160, 104], threshold = 120

## Run Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# runs on http://localhost:5173
```

