import { CalendarCheck, CheckCircle2, ChevronLeft, ChevronRight, Clock, NotebookText, RefreshCw, UserRound } from "lucide-react";
import { useContext, useEffect, useState } from "react";

import {
  getDoctorAppointmentsByStatus,
  getDoctorAppointmentsRange,
  getDoctorDashboard,
  getDoctorPatients,
  updateDoctorAppointmentStatus,
} from "../../api/index.js";
import Navbar from "../../components/Navbar.jsx";
import StatCard from "../../components/StatCard.jsx";
import { AppContext } from "../../context/AppContext.jsx";

const DoctorDashboard = () => {
  const [data, setData] = useState(null);
  const [patients, setPatients] = useState([]);
  const [appointments, setAppointments] = useState({ active: [], completed: [] });
  const [activeTab, setActiveTab] = useState("active");
  const [calendarMonth, setCalendarMonth] = useState(() => new Date());
  const [calendarAppointments, setCalendarAppointments] = useState([]);
  const [calendarLoading, setCalendarLoading] = useState(false);
  const { selectedDoctor } = useContext(AppContext);

  useEffect(() => {
    const doctorId = selectedDoctor?.id;
    if (!doctorId) {
      return;
    }
    Promise.all([
      getDoctorDashboard(doctorId),
      getDoctorPatients(doctorId),
      fetchAppointmentsByStatus(doctorId),
    ]).then(([dashboardResponse, patientsResponse]) => {
      setData(dashboardResponse.data);
      setPatients(patientsResponse.data.patients ?? []);
    });
  }, [selectedDoctor]);

  useEffect(() => {
    if (!selectedDoctor?.id) {
      return;
    }

    const handleFocus = () => {
      fetchAppointmentsRange(selectedDoctor.id, calendarMonth);
    };

    handleFocus();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [selectedDoctor, calendarMonth]);

  const fetchAppointmentsByStatus = async (doctorId) => {
    try {
      const response = await getDoctorAppointmentsByStatus(doctorId);
      setAppointments({
        active: response.data.active_appointments || [],
        completed: response.data.completed_appointments || []
      });
    } catch (error) {
      console.error("Error fetching appointments:", error);
    }
  };

  const handleStatusChange = async (appointmentId, nextStatus) => {
    try {
      await updateDoctorAppointmentStatus(appointmentId, nextStatus);
      fetchAppointmentsByStatus(selectedDoctor?.id);
    } catch (error) {
      console.error("Error toggling appointment status:", error);
    }
  };

  const formatDateKey = (dateValue) => {
    const year = dateValue.getFullYear();
    const month = String(dateValue.getMonth() + 1).padStart(2, "0");
    const day = String(dateValue.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const getMonthRange = (dateValue) => {
    const start = new Date(dateValue.getFullYear(), dateValue.getMonth(), 1);
    const end = new Date(dateValue.getFullYear(), dateValue.getMonth() + 1, 0);
    return { start, end };
  };

  const fetchAppointmentsRange = async (doctorId, monthDate) => {
    try {
      setCalendarLoading(true);
      const { start, end } = getMonthRange(monthDate);
      const response = await getDoctorAppointmentsRange(
        doctorId,
        formatDateKey(start),
        formatDateKey(end)
      );
      setCalendarAppointments(response.data.appointments ?? []);
    } catch (error) {
      console.error("Error fetching calendar appointments:", error);
    } finally {
      setCalendarLoading(false);
    }
  };

  const monthLabel = calendarMonth.toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  const dayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const monthStart = new Date(calendarMonth.getFullYear(), calendarMonth.getMonth(), 1);
  const gridStart = new Date(monthStart);
  gridStart.setDate(monthStart.getDate() - monthStart.getDay());

  const calendarDays = Array.from({ length: 42 }, (_, index) => {
    const day = new Date(gridStart);
    day.setDate(gridStart.getDate() + index);
    return day;
  });

  const appointmentsByDate = calendarAppointments.reduce((acc, appt) => {
    if (!acc[appt.date]) {
      acc[appt.date] = [];
    }
    acc[appt.date].push(appt);
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      <Navbar title="Doctor Dashboard" subtitle={selectedDoctor?.department ?? "Daily Overview"} />

      <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-950 to-slate-800 text-white p-6 sm:p-8 shadow-lg">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-300/80">Active doctor</p>
        <h3 className="text-2xl sm:text-3xl font-semibold mt-3">{selectedDoctor?.name ?? data?.doctor?.name ?? "Selected doctor"}</h3>
        <p className="text-slate-300 mt-2">
          {selectedDoctor?.department ?? data?.doctor?.department ?? "Department"}
          {selectedDoctor?.specialization ? ` • ${selectedDoctor.specialization}` : data?.doctor?.specialization ? ` • ${data.doctor.specialization}` : ""}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          label="Appointments today"
          value={data?.appointments_today ?? "--"}
          icon={CalendarCheck}
        />
        <StatCard
          label="Completed"
          value={data?.completed ?? "--"}
          icon={CheckCircle2}
          accent="text-green-600"
        />
        <StatCard
          label="Pending"
          value={data?.pending ?? "--"}
          icon={Clock}
          accent="text-amber-600"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 bg-white border border-slate-200 rounded-2xl p-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">Assigned patients calendar</p>
              <h3 className="text-xl font-semibold text-slate-900 mt-2">{monthLabel}</h3>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setCalendarMonth(new Date(calendarMonth.getFullYear(), calendarMonth.getMonth() - 1, 1))}
                className="h-9 w-9 rounded-full border border-slate-200 text-slate-500 hover:text-slate-900 hover:border-slate-300 transition"
                aria-label="Previous month"
              >
                <ChevronLeft className="h-4 w-4 mx-auto" />
              </button>
              <button
                type="button"
                onClick={() => setCalendarMonth(new Date())}
                className="px-3 py-2 rounded-full border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:border-slate-300 transition"
              >
                Today
              </button>
              <button
                type="button"
                onClick={() => setCalendarMonth(new Date(calendarMonth.getFullYear(), calendarMonth.getMonth() + 1, 1))}
                className="h-9 w-9 rounded-full border border-slate-200 text-slate-500 hover:text-slate-900 hover:border-slate-300 transition"
                aria-label="Next month"
              >
                <ChevronRight className="h-4 w-4 mx-auto" />
              </button>
              <button
                type="button"
                onClick={() => fetchAppointmentsRange(selectedDoctor?.id, calendarMonth)}
                className="inline-flex items-center gap-2 px-3 py-2 rounded-full border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:border-slate-300 transition"
              >
                <RefreshCw className={`h-4 w-4 ${calendarLoading ? "animate-spin" : ""}`} />
                Refresh
              </button>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-7 gap-2 text-xs font-semibold text-slate-500">
            {dayLabels.map((label) => (
              <div key={label} className="text-center">
                {label}
              </div>
            ))}
          </div>

          <div className="mt-3 grid grid-cols-7 gap-2">
            {calendarDays.map((day) => {
              const dateKey = formatDateKey(day);
              const dayAppointments = appointmentsByDate[dateKey] || [];
              const isCurrentMonth = day.getMonth() === calendarMonth.getMonth();
              const isToday = formatDateKey(new Date()) === dateKey;

              return (
                <div
                  key={dateKey}
                  className={`min-h-[7.5rem] rounded-xl border border-slate-200 p-2 text-xs transition ${
                    isCurrentMonth ? "bg-white" : "bg-slate-50 text-slate-400"
                  } ${isToday ? "border-cyan-400 shadow-sm" : ""}`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`text-xs font-semibold ${isCurrentMonth ? "text-slate-700" : "text-slate-400"}`}>
                      {day.getDate()}
                    </span>
                    {dayAppointments.length > 0 ? (
                      <span className="rounded-full bg-cyan-100 px-2 py-0.5 text-[10px] font-semibold text-cyan-700">
                        {dayAppointments.length}
                      </span>
                    ) : null}
                  </div>
                  <div className="mt-2 space-y-1">
                    {dayAppointments.slice(0, 3).map((appt) => (
                      <div key={appt.id} className="rounded-md bg-slate-100 px-2 py-1 text-[11px] text-slate-700">
                        <p className="font-semibold">{appt.time}</p>
                        <p className="truncate">{appt.patient_name}</p>
                      </div>
                    ))}
                    {dayAppointments.length > 3 ? (
                      <p className="text-[10px] text-slate-400">+{dayAppointments.length - 3} more</p>
                    ) : null}
                    {dayAppointments.length === 0 ? (
                      <p className="text-[10px] text-slate-300">No patients</p>
                    ) : null}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <div className="flex items-center gap-2">
            <UserRound className="h-5 w-5 text-cyan-600" />
            <h3 className="text-lg font-semibold text-slate-900">Assigned patients</h3>
          </div>
          <div className="mt-4 space-y-3 max-h-[52rem] overflow-auto pr-1">
            {patients.map((patient) => (
              <div key={patient.id} className="group rounded-2xl border border-slate-200 p-4 hover:border-cyan-300 hover:shadow-sm transition">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold text-slate-900">{patient.name}</p>
                    <p className="text-sm text-slate-500">Age {patient.age} • Visits {patient.visit_history}</p>
                    <p className="text-xs text-slate-400 mt-1">Next: {patient.summary?.next_appointment ?? "None scheduled"}</p>
                  </div>
                  <NotebookText className="h-5 w-5 text-slate-400 group-hover:text-cyan-600 transition" />
                </div>

                <div className="mt-3 space-y-2 text-sm text-slate-600">
                  <p>Blood group: {patient.blood_group ?? "--"}</p>
                  <p>Allergies: {patient.allergies ?? "--"}</p>
                  <p>Current medications: {patient.current_medications?.map((med) => med.name).join(", ") || "None"}</p>
                  <p>Conditions: {patient.existing_conditions?.join(", ") || "None"}</p>
                  <p>Phone: {patient.phone ?? "--"}</p>
                  <p>Previous meds: {patient.previous_medications?.map((med) => med.name).join(", ") || "None"}</p>
                  <div className="rounded-xl bg-slate-50 p-3 text-slate-600 mt-2">
                    <p className="font-medium text-slate-700">Latest consultation note:</p>
                    <p className="mt-1 text-sm">{patient.latest_consultation?.soap_notes ?? "No consultation yet"}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Recent consultations</h3>
          <div className="mt-4 space-y-3">
            {data?.recent_consultations?.map((consultation) => (
              <div key={consultation.id} className="rounded-2xl bg-slate-50 p-4">
                <p className="font-semibold text-slate-900">{consultation.patient}</p>
                <p className="text-sm text-slate-500 mt-1">{consultation.date}</p>
                <p className="text-sm text-slate-600 mt-2 whitespace-pre-line">{consultation.soap_notes}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Recent prescriptions</h3>
          <div className="mt-4 space-y-3">
            {data?.recent_prescriptions?.map((prescription) => (
              <div key={prescription.id} className="rounded-2xl bg-slate-50 p-4">
                <p className="font-semibold text-slate-900">{prescription.patient}</p>
                <p className="text-sm text-slate-500 mt-1">{prescription.date}</p>
                <p className="text-sm text-slate-600 mt-2">{prescription.notes}</p>
                <p className="text-xs text-slate-500 mt-2">
                  {prescription.medications?.map((med) => `${med.medication || med.name} ${med.dosage}`).join(" • ")}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Appointment Management Section */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Appointment Management</h3>
        
        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b border-slate-200">
          <button
            onClick={() => setActiveTab("active")}
            className={`px-4 py-2 text-sm font-semibold transition-colors ${
              activeTab === "active"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Active ({appointments.active.length})
          </button>
          <button
            onClick={() => setActiveTab("completed")}
            className={`px-4 py-2 text-sm font-semibold transition-colors ${
              activeTab === "completed"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Completed ({appointments.completed.length})
          </button>
        </div>

        {/* Active Appointments */}
        {activeTab === "active" && (
          <div className="space-y-3">
            {appointments.active.length > 0 ? (
              appointments.active.map((appt) => (
                <div key={appt.id} className="rounded-xl border border-blue-200 bg-blue-50 p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <p className="font-semibold text-slate-900">{appt.patient_name}</p>
                        <span className="px-2 py-1 text-xs font-semibold text-blue-700 bg-blue-100 rounded-full">
                          {appt.status}
                        </span>
                      </div>
                      <p className="text-sm text-slate-600 mt-1">
                        Age {appt.patient_age} | {appt.patient_phone}
                      </p>
                      <p className="text-sm text-slate-500 mt-2">
                        {appt.date} at {appt.time}
                      </p>
                      {appt.complaint && (
                        <p className="text-sm text-slate-600 mt-2">
                          <span className="font-medium">Complaint:</span> {appt.complaint}
                        </p>
                      )}
                      {appt.notes && (
                        <p className="text-sm text-slate-600 mt-2">
                          <span className="font-medium">Notes:</span> {appt.notes}
                        </p>
                      )}
                    </div>
                    <div className="ml-4" aria-label="Update appointment status">
                      <select
                        className="border border-slate-200 rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value="Active"
                        onChange={(e) => handleStatusChange(appt.id, e.target.value === "Completed" ? "Completed" : "Scheduled")}
                      >
                        <option value="Active">Active</option>
                        <option value="Completed">Completed</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500 text-center py-8">No active appointments for today</p>
            )}
          </div>
        )}

        {/* Completed Appointments */}
        {activeTab === "completed" && (
          <div className="space-y-3">
            {appointments.completed.length > 0 ? (
              appointments.completed.slice(0, 10).map((appt) => (
                <div key={appt.id} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <p className="font-semibold text-slate-900">{appt.patient_name}</p>
                        <span className="px-2 py-1 text-xs font-semibold text-slate-600 bg-slate-200 rounded-full">
                          {appt.status}
                        </span>
                      </div>
                      <p className="text-sm text-slate-600 mt-1">
                        Age {appt.patient_age}
                      </p>
                      <p className="text-sm text-slate-500 mt-2">
                        {appt.date} at {appt.time}
                      </p>
                      {appt.complaint && (
                        <p className="text-sm text-slate-600 mt-2">
                          <span className="font-medium">Complaint:</span> {appt.complaint}
                        </p>
                      )}
                      {appt.notes && (
                        <p className="text-sm text-slate-600 mt-2">
                          <span className="font-medium">Notes:</span> {appt.notes}
                        </p>
                      )}
                    </div>
                    <div className="ml-4" aria-label="Update appointment status">
                      <select
                        className="border border-slate-200 rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        value="Completed"
                        onChange={(e) => handleStatusChange(appt.id, e.target.value === "Completed" ? "Completed" : "Scheduled")}
                      >
                        <option value="Completed">Completed</option>
                        <option value="Active">Active</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500 text-center py-8">No completed appointments</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DoctorDashboard;
