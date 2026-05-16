import { useContext, useEffect, useState } from "react";
import Navbar from "../../components/Navbar.jsx";
import {
  getPatientAvailableDoctors,
  getPatientAvailableSlots,
  postPatientBookAppointment,
} from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const BookAppointment = () => {
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [appointmentDate, setAppointmentDate] = useState("");
  const [availableSlots, setAvailableSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState("");
  const [complaint, setComplaint] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const { selectedPatient } = useContext(AppContext);

  // Fetch available doctors on component mount
  useEffect(() => {
    fetchDoctors();
  }, []);

  // Fetch available slots when doctor and date are selected
  useEffect(() => {
    if (selectedDoctor && appointmentDate) {
      fetchAvailableSlots();
    } else {
      setAvailableSlots([]);
      setSelectedSlot("");
    }
  }, [selectedDoctor, appointmentDate]);

  const fetchDoctors = async () => {
    try {
      const response = await getPatientAvailableDoctors();
      setDoctors(response.data);
    } catch (err) {
      console.error("Error fetching doctors:", err);
      setError("Failed to load doctors. Please try again.");
    }
  };

  const fetchAvailableSlots = async () => {
    try {
      setLoading(true);
      const response = await getPatientAvailableSlots(selectedDoctor, appointmentDate);
      
      if (response.data.error) {
        setError(response.data.error);
        setAvailableSlots([]);
      } else {
        setAvailableSlots(response.data.available_slots || []);
        setError(null);
      }
    } catch (err) {
      console.error("Error fetching slots:", err);
      setError("Failed to load available slots.");
      setAvailableSlots([]);
    } finally {
      setLoading(false);
    }
  };

  const handleBookAppointment = async (e) => {
    e.preventDefault();

    if (!selectedPatient?.id) {
      setError("Please select a patient profile before booking.");
      return;
    }

    if (!selectedDoctor || !appointmentDate || !selectedSlot) {
      setError("Please fill in all required fields.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setMessage(null);

      const response = await postPatientBookAppointment({
        patient_id: selectedPatient.id,
        doctor_id: parseInt(selectedDoctor),
        appointment_date: appointmentDate,
        appointment_time: selectedSlot,
        complaint: complaint || null,
      });

      if (response.data.success) {
        setMessage({
          type: "success",
          text: response.data.message,
          appointment: response.data.appointment,
        });
        
        // Reset form
        setSelectedDoctor("");
        setAppointmentDate("");
        setSelectedSlot("");
        setComplaint("");
        setAvailableSlots([]);
      } else if (response.data.error) {
        setError(response.data.error);
      }
    } catch (err) {
      console.error("Error booking appointment:", err);
      setError(err.response?.data?.error || "Failed to book appointment. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Get minimum date (today)
  const getMinDate = () => {
    const today = new Date();
    return today.toISOString().split("T")[0];
  };

  // Get maximum date (3 months from now)
  const getMaxDate = () => {
    const maxDate = new Date();
    maxDate.setMonth(maxDate.getMonth() + 3);
    return maxDate.toISOString().split("T")[0];
  };

  const selectedDoctorInfo = doctors.find((doc) => doc.id === parseInt(selectedDoctor));

  return (
    <div className="space-y-8">
      <Navbar title="Book Appointment" subtitle="Schedule Your Visit" />

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Success Message */}
      {message && message.type === "success" && (
        <div className="bg-green-50 border border-green-200 rounded-2xl p-6">
          <p className="text-sm uppercase tracking-[0.2em] text-green-600 font-semibold">Success</p>
          <h3 className="text-lg font-semibold text-slate-900 mt-2">{message.text}</h3>
          {message.appointment && (
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              <p><strong>Doctor:</strong> {message.appointment.doctor_name} ({message.appointment.doctor_specialization})</p>
              <p><strong>Department:</strong> {message.appointment.department}</p>
              <p><strong>Date:</strong> {message.appointment.date}</p>
              <p><strong>Time:</strong> {message.appointment.time}</p>
              {message.appointment.complaint && (
                <p><strong>Reason:</strong> {message.appointment.complaint}</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Booking Form */}
      <form onSubmit={handleBookAppointment} className="bg-white border border-slate-200 rounded-2xl p-6 space-y-6">
        {/* Step 1: Select Doctor */}
        <div>
          <p className="text-sm text-slate-500">Step 1</p>
          <label className="text-sm font-semibold text-slate-700">Select Doctor</label>
          <select
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={selectedDoctor}
            onChange={(e) => {
              setSelectedDoctor(e.target.value);
              setSelectedSlot("");
            }}
            required
          >
            <option value="">Choose a doctor</option>
            {doctors.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.name} - {doc.specialization} ({doc.department})
              </option>
            ))}
          </select>
        </div>

        {/* Step 2: Select Date */}
        <div>
          <p className="text-sm text-slate-500">Step 2</p>
          <label className="text-sm font-semibold text-slate-700">Select Date</label>
          <input
            type="date"
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={appointmentDate}
            onChange={(e) => {
              setAppointmentDate(e.target.value);
              setSelectedSlot("");
            }}
            min={getMinDate()}
            max={getMaxDate()}
            disabled={!selectedDoctor}
            required
          />
        </div>

        {/* Step 3: Select Time Slot */}
        <div>
          <p className="text-sm text-slate-500">Step 3</p>
          <label className="text-sm font-semibold text-slate-700">Select Time Slot</label>
          {loading && appointmentDate && selectedDoctor ? (
            <p className="mt-2 text-sm text-slate-500">Loading available slots...</p>
          ) : (
            <select
              className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={selectedSlot}
              onChange={(e) => setSelectedSlot(e.target.value)}
              disabled={!appointmentDate || availableSlots.length === 0}
              required
            >
              <option value="">Choose a time slot</option>
              {availableSlots.map((slot) => (
                <option key={slot} value={slot}>
                  {slot}
                </option>
              ))}
            </select>
          )}
          {appointmentDate && selectedDoctor && availableSlots.length === 0 && !loading && (
            <p className="mt-2 text-sm text-orange-600">No available slots for this date. Please select another date.</p>
          )}
        </div>

        {/* Step 4: Reason for Visit (Optional) */}
        <div>
          <p className="text-sm text-slate-500">Step 4 (Optional)</p>
          <label className="text-sm font-semibold text-slate-700">Reason for Visit</label>
          <textarea
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            placeholder="Describe your symptoms or reason for visit..."
            rows="3"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !selectedDoctor || !appointmentDate || !selectedSlot}
          className="w-full bg-blue-600 text-white rounded-xl px-4 py-3 text-sm font-semibold hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Booking..." : "Book Appointment"}
        </button>
      </form>

      {/* Selected Doctor Info */}
      {selectedDoctorInfo && (
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-400">Selected Doctor</p>
          <h3 className="text-lg font-semibold text-slate-900 mt-2">{selectedDoctorInfo.name}</h3>
          <p className="text-sm text-slate-600 mt-1">
            {selectedDoctorInfo.specialization} | {selectedDoctorInfo.department}
          </p>
        </div>
      )}
    </div>
  );
};

export default BookAppointment;

// Made with Bob
