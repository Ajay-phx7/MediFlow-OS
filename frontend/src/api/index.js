import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  if (typeof window === "undefined") {
    return config;
  }

  try {
    const role = JSON.parse(window.localStorage.getItem("mediflow.activeRole") || "null");
    const doctor = JSON.parse(window.localStorage.getItem("mediflow.selectedDoctor") || "null");
    const patient = JSON.parse(window.localStorage.getItem("mediflow.selectedPatient") || "null");
    const userId = role === "doctor" ? doctor?.id : role === "patient" ? patient?.id : null;

    if (role && userId) {
      config.headers["X-User-Role"] = role;
      config.headers["X-User-Id"] = String(userId);
    }
  } catch {
    // If localStorage is unavailable, skip headers.
  }

  return config;
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
export const getDoctorAppointmentsByStatus = (doctorId) =>
  api.get("/api/doctor/appointments-by-status", { params: doctorId ? { doctor_id: doctorId } : undefined });
export const getDoctorAppointmentsRange = (doctorId, startDate, endDate) =>
  api.get("/api/doctor/appointments-range", {
    params: doctorId
      ? {
          doctor_id: doctorId,
          start_date: startDate,
          end_date: endDate,
        }
      : undefined,
  });
export const updateDoctorAppointmentStatus = (appointmentId, status) =>
  api.put(`/api/doctor/appointment/${appointmentId}/status`, { status });

export const getPatientDashboard = (patientId) =>
  api.get("/api/patient/dashboard", { params: patientId ? { patient_id: patientId } : undefined });
export const getPatientHealthReport = (patientId) =>
  api.get("/api/patient/health-report", { params: patientId ? { patient_id: patientId } : undefined });
export const getPatientAvailableDoctors = () => api.get("/api/patient/doctors");
export const getPatientAvailableSlots = (doctorId, appointmentDate) =>
  api.get("/api/patient/available-slots", {
    params: { doctor_id: doctorId, appointment_date: appointmentDate },
  });
export const postPatientBookAppointment = (payload) => api.post("/api/patient/book-appointment", payload);

export default api;
