# AI-Powered Medical Scribe Application

## Overview

An AI-powered medical scribe application that listens to conversations between doctors and patients during consultations and automatically generates structured medical prescriptions and clinical notes in real-time using IBM Speech-to-Text and Google Gemini AI.

## Features

### ✅ Implemented Features

1. **Live Audio Capture**
   - Real-time microphone recording in browser
   - Pause/Resume functionality
   - Recording timer
   - Audio file upload support

2. **IBM Speech-to-Text Integration**
   - Real-time streaming transcription
   - Speaker diarization (Doctor vs Patient)
   - Timestamped transcripts
   - Medical vocabulary optimization
   - Noise filtering support

3. **AI Medical Understanding**
   - Automatic extraction of:
     - Symptoms
     - Diagnoses
     - Medications with dosages
     - Tests recommended
     - Follow-up instructions
     - Allergies
     - Duration of illness
     - Vitals

4. **Document Generation**
   - **Prescription**: Clean, structured prescription with medications, dosages, and instructions
   - **SOAP Notes**: Subjective, Objective, Assessment, Plan format
   - Both documents are editable before saving

5. **Real-time Processing**
   - WebSocket-based live transcription
   - Instant transcript updates
   - Speaker identification

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  AIScribe Component                                     │ │
│  │  - Audio Recording Controls                             │ │
│  │  - Real-time Transcript Display                         │ │
│  │  - Editable Notes & Prescription                        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ WebSocket / HTTP
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  WebSocket Endpoint                                     │ │
│  │  - Real-time audio streaming                            │ │
│  │  - Live transcription updates                           │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  REST API Endpoints                                     │ │
│  │  - /api/doctor/scribe (text)                            │ │
│  │  - /api/doctor/scribe/audio (file upload)               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Services Layer                         │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │ IBM Watson           │  │ Google Gemini 1.5 Pro         │ │
│  │ Speech-to-Text       │  │ Medical Entity Extraction     │ │
│  │ - Transcription      │  │ - SOAP Notes Generation       │ │
│  │ - Speaker Diarization│  │ - Prescription Generation     │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- IBM Watson Speech-to-Text account
- Google Gemini API account

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure API keys:**

Create a `.env` file in the `backend` directory:

```env
# IBM Watson Speech-to-Text Configuration
IBM_SPEECH_TO_TEXT_API_KEY=your_ibm_api_key_here
IBM_SPEECH_TO_TEXT_URL=https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/your-instance-id

# Grok / Groq fallback for speech-to-text if IBM is unavailable
GROK_API_KEY=your_grok_api_key_here
# or
GROQ_API_KEY=your_groq_api_key_here

# Google Gemini Configuration
GEMINI_API_KEYS=your_gemini_api_key_here,your_second_gemini_key_here,your_third_gemini_key_here,your_fourth_gemini_key_here
# GEMINI_API_KEY=your_gemini_api_key_here  # single-key fallback is still supported

# Application Configuration
ENVIRONMENT=development
```

3. **Start the backend server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start the development server:**
```bash
npm run dev
```

3. **Access the application:**
Open http://localhost:5173 in your browser

## Usage

### Mode 1: Text Input

1. Navigate to AI Scribe page
2. Select "Text Input" mode
3. Paste or type the consultation transcript
4. Click "Generate Notes & Prescription"
5. Review and edit the generated documents
6. Save the prescription

### Mode 2: Real-time Audio Recording

1. Navigate to AI Scribe page
2. Select "Audio Recording" mode
3. Choose "Real-time Transcription"
4. Click "Start Recording"
5. Speak naturally during the consultation
6. View live transcript with speaker labels
7. Click "Stop Recording" when done
8. Click "Generate Notes & Prescription"
9. Review and edit the documents

### Mode 3: Audio File Upload

1. Navigate to AI Scribe page
2. Select "Audio Recording" mode
3. Choose "Upload Audio File"
4. Select an audio file (WAV, MP3, FLAC, OGG)
5. Wait for processing
6. Review the transcript and generated documents

## API Endpoints

### REST API

#### POST `/api/doctor/scribe`
Process text transcript and generate medical documents

**Request:**
```json
{
  "transcript": "Doctor: What symptoms are you experiencing?\nPatient: I have had a fever for three days.",
  "patient_name": "John Doe",
  "patient_age": 35
}
```

**Response:**
```json
{
  "notes": "S: Patient reports fever for 3 days...",
  "prescription": [
    {
      "medication": "Paracetamol 500mg",
      "dosage": "Twice daily",
      "duration": "5 days"
    }
  ],
  "entities": {...},
  "mode": "ai"
}
```

#### POST `/api/doctor/scribe/audio`
Upload audio file for transcription and processing

**Request:** Multipart form data
- `audio`: Audio file (WAV, MP3, FLAC, OGG)
- `patient_name`: Optional patient name
- `patient_age`: Optional patient age

**Response:**
```json
{
  "transcription": {
    "transcript": "Full transcript text",
    "formatted_transcript": "Doctor: ...\nPatient: ...",
    "speaker_segments": [...]
  },
  "notes": "SOAP notes",
  "prescription": [...],
  "mode": "ai"
}
```

### WebSocket API

#### WS `/api/ws/scribe/{client_id}`
Real-time audio streaming and transcription

**Client sends:** Binary audio chunks

**Server sends:**
```json
{
  "type": "transcript_update",
  "transcript": "Doctor: What symptoms...",
  "speaker_segments": [...],
  "is_final": true
}
```

## File Structure

```
backend/
├── config.py                          # Configuration management
├── main.py                            # FastAPI application
├── requirements.txt                   # Python dependencies
├── services/
│   ├── doctor_service.py              # Doctor service logic
│   ├── speech_to_text_service.py      # IBM Watson integration
│   └── medical_ai_service.py          # OpenAI medical AI
└── routers/
    ├── doctor.py                      # Doctor endpoints
    └── websocket_scribe.py            # WebSocket endpoint

frontend/
└── src/
    └── pages/
        └── doctor/
            └── AIScribe.jsx           # Main AI Scribe component
```

## Key Components

### Backend Services

#### `SpeechToTextService`
- Handles IBM Watson Speech-to-Text integration
- Provides speaker diarization
- Formats transcripts with speaker labels
- Supports both file and stream transcription

#### `MedicalAIService`
- Extracts medical entities using Google Gemini 1.5 Pro
- Generates SOAP notes
- Creates structured prescriptions
- Analyzes transcript quality

#### `DoctorService`
- Orchestrates the AI pipeline
- Handles fallback to mock data
- Processes audio files
- Manages patient information

### Frontend Components

#### `AIScribe.jsx`
- Audio recording controls
- Real-time transcript display
- WebSocket connection management
- Editable notes and prescription
- Multiple input modes

## Configuration

### IBM Watson Speech-to-Text

1. Create an IBM Cloud account
2. Create a Speech-to-Text service instance
3. Copy the API key and URL
4. Add to `.env` file

### Google Gemini API

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Add to `.env` file as `GEMINI_API_KEYS`

## Error Handling

The application includes comprehensive error handling:

- **API not configured**: Falls back to mock data
- **Microphone access denied**: Shows user-friendly error
- **WebSocket connection failed**: Displays connection error
- **Transcription errors**: Logs and displays error messages
- **File upload errors**: Validates file type and size

## Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **CORS**: Configure allowed origins in production
3. **File Upload**: Validate file types and sizes
4. **WebSocket**: Implement authentication in production
5. **Data Privacy**: Ensure HIPAA compliance for medical data

## Performance Optimization

1. **Audio Chunking**: Processes audio in 1-second chunks
2. **Lazy Loading**: Services loaded only when needed
3. **WebSocket**: Efficient real-time communication
4. **Caching**: Singleton pattern for service instances

## Future Enhancements

- [ ] Database integration for storing consultations
- [ ] User authentication and authorization
- [ ] Multi-language support
- [ ] Custom medical vocabulary training
- [ ] Integration with EHR systems
- [ ] Voice commands for hands-free operation
- [ ] Automated ICD-10 coding
- [ ] Drug interaction checking
- [ ] Patient consent management

## Troubleshooting

### Issue: "API keys not configured"
**Solution:** Create `.env` file with valid API keys

### Issue: "Microphone not accessible"
**Solution:** Grant microphone permissions in browser settings

### Issue: "WebSocket connection failed"
**Solution:** Ensure backend server is running on port 8000

### Issue: "Import errors in Python"
**Solution:** Install all dependencies: `pip install -r requirements.txt`

## License

This project is part of MediFlow OS.

## Support

For issues and questions, please refer to the main project documentation.

---

**Made with Bob** 🤖