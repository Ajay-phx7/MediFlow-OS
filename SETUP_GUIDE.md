# MediFlow OS - Setup Guide

Complete guide to setting up and running the MediFlow OS hospital management system.

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 16.x or higher
- npm or yarn

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MediFlow-OS
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Required Python Packages

The `requirements.txt` includes:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - Form data handling
- `prophet` - Time series forecasting (for surge prediction)
- `pandas` - Data manipulation
- `numpy` - Numerical computing

#### Install Prophet (Optional - for ML features)

Prophet requires additional dependencies:

**Windows:**
```bash
pip install prophet
```

**macOS/Linux:**
```bash
pip install prophet
```

If you encounter issues with Prophet installation, see the [Prophet Installation Guide](https://facebook.github.io/prophet/docs/installation.html).

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Required npm Packages

The frontend uses:
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- Lucide React (icons)
- React Router (routing)

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Project Structure

```
MediFlow-OS/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── ml/                     # Machine learning modules
│   │   ├── __init__.py
│   │   ├── surge_model.py      # Patient surge prediction
│   │   └── training_data.py    # Training data generation
│   ├── mock_data/              # Mock data for development
│   │   ├── departments.py
│   │   ├── doctors.py
│   │   ├── patients.py
│   │   ├── queue.py
│   │   ├── emergency.py
│   │   └── weekly_report.py
│   └── routers/                # API route handlers
│       ├── admin.py
│       ├── doctor.py
│       └── patient.py
├── frontend/
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main app component
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   │   ├── admin/
│   │   │   ├── doctor/
│   │   │   └── patient/
│   │   ├── context/            # React context
│   │   └── api/                # API client
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Configuration

### Backend Configuration

Edit `backend/main.py` to configure:
- CORS settings
- API routes
- Database connections (when implemented)

### Frontend Configuration

Edit `frontend/src/api/index.js` to configure:
- API base URL
- Request interceptors
- Error handling

## Features

### Admin Dashboard
- Real-time hospital statistics
- Patient queue management
- Department monitoring
- Surge prediction with Prophet ML
- Emergency control center
- Weekly performance reports

### Doctor Portal
- Patient list management
- AI-powered medical scribe
- Patient records access

### Patient Portal
- Appointment booking
- Health reports
- Hospital congestion map
- Real-time wait times

## Machine Learning Features

### Patient Surge Prediction

The system uses Facebook Prophet for time series forecasting to predict patient surges.

**Training the Model:**

```python
from ml.surge_model import get_surge_predictor
from ml.training_data import get_training_data

predictor = get_surge_predictor()
training_data = get_training_data()
predictor.train(training_data)
```

**Making Predictions:**

```python
forecast = predictor.predict_with_threshold(days_ahead=7, threshold=120)
```

See [PROPHET_TESTING_GUIDE.md](PROPHET_TESTING_GUIDE.md) for detailed testing instructions.

## API Endpoints

### Admin Routes (`/api/admin`)
- `GET /stats` - Hospital statistics
- `GET /queue` - Patient queue
- `GET /surge-forecast` - Surge predictions
- `GET /live-map` - Department status
- `GET /emergency/alerts` - Emergency alerts
- `GET /emergency/protocols` - Emergency protocols
- `GET /weekly-report` - Weekly performance report

### Doctor Routes (`/api/doctor`)
- `GET /patients` - Patient list
- `GET /stats` - Doctor statistics

### Patient Routes (`/api/patient`)
- `GET /appointments` - Patient appointments
- `GET /congestion` - Hospital congestion data

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Prophet installation fails:**
- Ensure you have a C++ compiler installed
- Try installing via conda: `conda install -c conda-forge prophet`

### Frontend Issues

**Port 5173 already in use:**
```bash
# Vite will automatically try the next available port
npm run dev
```

**Module not found errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Tips

1. **Hot Reload**: Both backend and frontend support hot reload during development
2. **API Testing**: Use the Swagger UI at `http://localhost:8000/docs` to test API endpoints
3. **Mock Data**: All data is currently mocked in the `backend/mock_data/` directory
4. **Styling**: Use TailwindCSS utility classes for consistent styling

## Production Deployment

### Backend

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The built files will be in `frontend/dist/` and can be served by any static file server.

## Next Steps

1. Set up a real database (PostgreSQL recommended)
2. Implement authentication and authorization
3. Add real-time features with WebSockets
4. Deploy to cloud infrastructure
5. Set up monitoring and logging
6. Implement data backup strategies

## Support

For issues and questions:
- Check the [README.md](README.md) for project overview
- Review [PROPHET_IMPLEMENTATION_SUMMARY.md](PROPHET_IMPLEMENTATION_SUMMARY.md) for ML details
- Open an issue on the project repository

## License

[Add your license information here]