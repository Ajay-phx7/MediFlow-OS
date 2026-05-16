# MediFlow OS

MediFlow OS is a full-stack Hospital Management Platform with AI-powered medical scribe features.

## 🆕 AI-Powered Medical Scribe

Live audio recording → Real-time transcription → Automatic SOAP notes & prescriptions

📖 **[Full Documentation](README_AI_SCRIBE.md)** | 🚀 **[Setup Guide](SETUP_GUIDE.md)**

## Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI (Python) + WebSocket
- **AI**: IBM Watson Speech-to-Text + OpenAI GPT-4o-mini

## Project Structure

```
backend/
	main.py, config.py, requirements.txt
	routers/          # API endpoints
	services/         # Business logic + AI integration
	mock_data/        # Demo data

frontend/
	src/
		pages/        # Admin, Doctor, Patient dashboards
		components/   # Reusable UI components
```

## Quick Start

### Demo Mode (No API Keys)
```bash
# Backend
cd backend
pip install fastapi uvicorn python-multipart
uvicorn main:app --reload

# Frontend
cd frontend
npm install && npm run dev
```

### Full AI Mode
```bash
cd backend
pip install -r requirements.txt

# Create .env with API keys (see .env.example)
uvicorn main:app --reload
```

Access at: http://localhost:5173

## API Endpoints

**Mock Data:**
- `GET /api/admin/*` - Admin dashboard, queue, surge forecast, live map
- `GET /api/doctor/*` - Doctor dashboard, patients list
- `GET /api/patient/*` - Patient dashboard, health report

**AI Features:**
- `POST /api/doctor/scribe` - Text transcript → SOAP notes + prescription
- `POST /api/doctor/scribe/audio` - Audio file → Transcription + documents
- `WS /api/ws/scribe/{id}` - Real-time audio streaming

## Features

**Admin**: Queue management, surge prediction, live congestion map  
**Doctor**: Patient list, AI scribe (audio recording, transcription, SOAP notes, prescriptions)  
**Patient**: Appointment booking, health reports, wait time estimates

## Documentation

- [AI Scribe Documentation](README_AI_SCRIBE.md) - Complete feature guide
- [Setup Guide](SETUP_GUIDE.md) - Installation & troubleshooting
- [API Docs](http://localhost:8000/docs) - Interactive API documentation

## Notes

- No database or auth (demo purposes)
- AI features work with mock data when API keys not configured
- CORS enabled for localhost:5173
- Requires HTTPS in production for microphone access

---

**Made with Bob** 🤖
