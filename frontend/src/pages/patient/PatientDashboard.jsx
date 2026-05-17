import { useContext, useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import {
  cancelPatientAppointment,
  getPatientAvailableSlots,
  getPatientDashboard,
  reschedulePatientAppointment,
} from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientDashboard = () => {
  const [data, setData] = useState(null);
  const [actionMessage, setActionMessage] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [rescheduleTarget, setRescheduleTarget] = useState(null);
  const [rescheduleDate, setRescheduleDate] = useState("");
  const [rescheduleSlot, setRescheduleSlot] = useState("");
  const [rescheduleSlots, setRescheduleSlots] = useState([]);
  const [rescheduleLoading, setRescheduleLoading] = useState(false);
  const { selectedPatient } = useContext(AppContext);

  useEffect(() => {
    if (!selectedPatient?.id) {
      return;
    }
    getPatientDashboard(selectedPatient.id).then((response) => setData(response.data));
  }, [selectedPatient]);

  useEffect(() => {
    const fetchSlots = async () => {
      if (!rescheduleTarget?.doctor_id || !rescheduleDate) {
        setRescheduleSlots([]);
        return;
      }

      try {
        setRescheduleLoading(true);
        const response = await getPatientAvailableSlots(rescheduleTarget.doctor_id, rescheduleDate);
        if (response.data.error) {
          setActionError(response.data.error);
          setRescheduleSlots([]);
        } else {
          setRescheduleSlots(response.data.available_slots ?? []);
        }
      } catch (error) {
        console.error("Error fetching slots:", error);
        setActionError("Failed to load available slots.");
        setRescheduleSlots([]);
      } finally {
        setRescheduleLoading(false);
      }
    };

    fetchSlots();
  }, [rescheduleTarget, rescheduleDate]);

  const refreshDashboard = async () => {
    if (!selectedPatient?.id) return;
    const response = await getPatientDashboard(selectedPatient.id);
    setData(response.data);
  };

  const handleCancelAppointment = async (appointmentId) => {
    if (!selectedPatient?.id) return;
    setActionError(null);
    setActionMessage(null);

    try {
      const response = await cancelPatientAppointment(appointmentId, selectedPatient.id);
      if (response.data.error) {
        setActionError(response.data.error);
      } else {
        setActionMessage(response.data.message ?? "Appointment cancelled.");
        setRescheduleTarget(null);
      }
    } catch (error) {
      console.error("Error cancelling appointment:", error);
      setActionError(error.response?.data?.error || "Failed to cancel appointment.");
    } finally {
      refreshDashboard();
    }
  };

  const handleRescheduleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedPatient?.id || !rescheduleTarget?.id) return;

    setActionError(null);
    setActionMessage(null);

    try {
      const response = await reschedulePatientAppointment(rescheduleTarget.id, {
        patient_id: selectedPatient.id,
        appointment_date: rescheduleDate,
        appointment_time: rescheduleSlot,
      });

      if (response.data.error) {
        setActionError(response.data.error);
        return;
      }

      setActionMessage(response.data.message ?? "Appointment rescheduled.");
      setRescheduleTarget(null);
      setRescheduleDate("");
      setRescheduleSlot("");
      setRescheduleSlots([]);
    } catch (error) {
      console.error("Error rescheduling appointment:", error);
      setActionError(error.response?.data?.error || "Failed to reschedule appointment.");
    } finally {
      refreshDashboard();
    }
  };

  return (
    <div className="space-y-8">
      <Navbar
        title="Patient Dashboard"
        subtitle={selectedPatient?.name ?? "Welcome Back"}
        displayName={data?.patient?.name ?? selectedPatient?.name}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Hello, {data?.patient?.name ?? "--"}</h3>
          <p className="text-sm text-slate-600 mt-2">Here is your linked doctor and upcoming appointment.</p>
          <div className="mt-4 bg-slate-50 rounded-xl p-4">
            <p className="text-sm text-slate-500">Linked doctor</p>
            <p className="text-base font-semibold text-slate-900">{data?.linked_doctor?.name ?? "--"}</p>
            <p className="text-sm text-slate-600 mt-1">{data?.linked_doctor?.department ?? "--"}</p>
          </div>
          <div className="mt-4 bg-slate-50 rounded-xl p-4">
            <p className="text-sm text-slate-500">Doctor</p>
            <p className="text-base font-semibold text-slate-900">
              {data?.upcoming_appointments?.[0]?.doctor ?? "--"}
            </p>
            <p className="text-sm text-slate-600 mt-1">
              {data?.upcoming_appointments?.[0]?.department ?? "--"} | {data?.upcoming_appointments?.[0]?.time ?? "--"}
            </p>
            <p className="text-sm text-slate-500 mt-2">{data?.upcoming_appointments?.[0]?.complaint ?? "No upcoming appointment"}</p>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Current medications</h3>
          <ul className="mt-4 space-y-2">
            {data?.current_medications?.map((item) => (
              <li key={item.name} className="text-sm text-slate-600">
                - {item.name} {item.dosage}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Recent prescriptions</h3>
          <div className="mt-4 space-y-3">
            {data?.recent_prescriptions?.map((prescription) => (
              <div key={prescription.id} className="rounded-2xl bg-slate-50 p-4">
                <p className="font-semibold text-slate-900">{prescription.doctor}</p>
                <p className="text-sm text-slate-500 mt-1">{prescription.date}</p>
                <p className="text-xs text-slate-500 mt-2">
                  {prescription.medications?.map((med) => `${med.name} ${med.dosage}`).join(" • ")}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Recent consultations</h3>
          <div className="mt-4 space-y-3">
            {data?.recent_consultations?.map((consultation) => (
              <div key={consultation.id} className="rounded-2xl bg-slate-50 p-4">
                <p className="font-semibold text-slate-900">{consultation.doctor}</p>
                <p className="text-sm text-slate-500 mt-1">{consultation.date}</p>
                <p className="text-sm text-slate-600 mt-2">{consultation.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Appointments Section */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900">My Appointments</h3>
          <a
            href="/patient/book-appointment"
            className="text-sm text-blue-600 hover:text-blue-700 font-semibold"
          >
            Book New Appointment →
          </a>
        </div>
        
        {/* Upcoming Appointments */}
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-700 mb-3">Upcoming</h4>
          {actionError && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              {actionError}
            </div>
          )}
          {actionMessage && (
            <div className="mb-4 rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
              {actionMessage}
            </div>
          )}
          <div className="space-y-3">
            {data?.upcoming_appointments && data.upcoming_appointments.length > 0 ? (
              data.upcoming_appointments.map((appt) => (
                <div key={appt.id} className="rounded-xl bg-blue-50 border border-blue-200 p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-slate-900">{appt.doctor}</p>
                      <p className="text-sm text-slate-600 mt-1">{appt.department}</p>
                      <p className="text-sm text-slate-500 mt-2">
                        {appt.date} at {appt.time}
                      </p>
                      {appt.complaint && (
                        <p className="text-sm text-slate-600 mt-2">
                          <span className="font-medium">Reason:</span> {appt.complaint}
                        </p>
                      )}
                    </div>
                    <span className="px-3 py-1 text-xs font-semibold text-blue-700 bg-blue-100 rounded-full">
                      {appt.status}
                    </span>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => handleCancelAppointment(appt.id)}
                      className="rounded-full border border-red-200 px-4 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-50"
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setRescheduleTarget(appt);
                        setRescheduleDate("");
                        setRescheduleSlot("");
                        setRescheduleSlots([]);
                        setActionError(null);
                        setActionMessage(null);
                      }}
                      className="rounded-full border border-blue-200 px-4 py-1.5 text-xs font-semibold text-blue-700 hover:bg-blue-100"
                    >
                      Reschedule
                    </button>
                  </div>
                  {rescheduleTarget?.id === appt.id && (
                    <form onSubmit={handleRescheduleSubmit} className="mt-4 rounded-xl bg-white p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">New slot</p>
                      <div className="mt-3 grid gap-3 sm:grid-cols-2">
                        <label className="text-xs font-semibold text-slate-600">
                          Date
                          <input
                            type="date"
                            className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm"
                            value={rescheduleDate}
                            onChange={(event) => {
                              setRescheduleDate(event.target.value);
                              setRescheduleSlot("");
                            }}
                            required
                          />
                        </label>
                        <label className="text-xs font-semibold text-slate-600">
                          Time slot
                          <select
                            className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm"
                            value={rescheduleSlot}
                            onChange={(event) => setRescheduleSlot(event.target.value)}
                            required
                          >
                            <option value="">Select a slot</option>
                            {rescheduleSlots.map((slot) => (
                              <option key={slot} value={slot}>{slot}</option>
                            ))}
                          </select>
                        </label>
                      </div>
                      {rescheduleLoading && (
                        <p className="mt-3 text-xs text-slate-500">Loading available slots...</p>
                      )}
                      <div className="mt-4 flex flex-wrap gap-2">
                        <button
                          type="submit"
                          disabled={!rescheduleDate || !rescheduleSlot}
                          className="rounded-full bg-blue-600 px-4 py-2 text-xs font-semibold text-white disabled:opacity-50"
                        >
                          Confirm reschedule
                        </button>
                        <button
                          type="button"
                          onClick={() => setRescheduleTarget(null)}
                          className="rounded-full border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600"
                        >
                          Close
                        </button>
                      </div>
                    </form>
                  )}
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">No upcoming appointments</p>
            )}
          </div>
        </div>

        {/* Past Appointments */}
        <div>
          <h4 className="text-sm font-semibold text-slate-700 mb-3">Past Appointments</h4>
          <div className="space-y-3">
            {data?.past_appointments && data.past_appointments.length > 0 ? (
              data.past_appointments.slice(0, 3).map((appt) => (
                <div key={appt.id} className="rounded-xl bg-slate-50 p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-slate-900">{appt.doctor}</p>
                      <p className="text-sm text-slate-500 mt-1">{appt.date}</p>
                      {appt.complaint && (
                        <p className="text-sm text-slate-600 mt-2">{appt.complaint}</p>
                      )}
                    </div>
                    <span className="px-3 py-1 text-xs font-semibold text-slate-600 bg-slate-200 rounded-full">
                      {appt.status}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">No past appointments</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
