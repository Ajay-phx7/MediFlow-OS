import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const getAdminStats = () => api.get("/api/admin/stats");
export const getAdminQueue = () => api.get("/api/admin/queue");
export const getAdminSurgeForecast = () => api.get("/api/admin/surge-forecast");
export const getSurgeForecastCustom = (days) =>
  api.post("/api/admin/surge-forecast/custom", { days });
export const getAdminLiveMap = () => api.get("/api/admin/live-map");

export const getEmergencyAlerts = () => api.get("/api/admin/emergency/alerts");
export const getEmergencyResources = () => api.get("/api/admin/emergency/resources");
export const escalateAlert = (alertId, level) =>
  api.post("/api/admin/emergency/escalate", { alertId, level });
export const getProtocol = (type) =>
  api.get("/api/admin/emergency/protocol", { params: { type } });

export const getDoctorDashboard = () => api.get("/api/doctor/dashboard");
export const getDoctorPatients = () => api.get("/api/doctor/patients");
export const postDoctorScribe = (payload) => api.post("/api/doctor/scribe", payload);

export const getPatientDashboard = () => api.get("/api/patient/dashboard");
export const getPatientHealthReport = () => api.get("/api/patient/health-report");

export default api;
