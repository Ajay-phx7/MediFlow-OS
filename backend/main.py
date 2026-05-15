from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import admin, doctor, patient

app = FastAPI(title="MediCore API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(doctor.router, prefix="/api/doctor", tags=["doctor"])
app.include_router(patient.router, prefix="/api/patient", tags=["patient"])


@app.get("/")
def read_root():
    return {"status": "MediCore API running"}
