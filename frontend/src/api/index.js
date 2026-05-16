import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const getAdminStats = () => api.get("/api/admin/stats");
export const getAdminQueue = () => api.get("/api/admin/queue");
export const getAdminSurgeForecast = () => api.get("/api/admin/surge-forecast");
export const getAdminLiveMap = () => api.get("/api/admin/live-map");

export const getAvailableDoctors = () => api.get("/api/auth/doctors");
export const loginAsDoctor = (doctorId) => api.get(`/api/auth/doctors/${doctorId}`);

export const getAvailablePatients = (search = "") =>
  api.get("/api/auth/patients", { params: search ? { search } : undefined });
export const loginAsPatient = (patientId) => api.get(`/api/auth/patients/${patientId}`);

export const getDoctorDashboard = (doctorId) =>
  api.get("/api/doctor/dashboard", { params: doctorId ? { doctor_id: doctorId } : undefined });
export const getDoctorPatients = (doctorId) =>
  api.get("/api/doctor/patients", { params: doctorId ? { doctor_id: doctorId } : undefined });
export const postDoctorScribe = (payload) => api.post("/api/doctor/scribe", payload);

export const getPatientDashboard = (patientId) =>
  api.get("/api/patient/dashboard", { params: patientId ? { patient_id: patientId } : undefined });
export const getPatientHealthReport = (patientId) =>
  api.get("/api/patient/health-report", { params: patientId ? { patient_id: patientId } : undefined });

export default api;
