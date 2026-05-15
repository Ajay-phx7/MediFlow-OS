import { useMemo, useState } from "react";

import Navbar from "../../components/Navbar.jsx";

const DEPARTMENTS = [
  "Cardiology",
  "Orthopaedics",
  "Paediatrics",
  "Emergency",
];

const DOCTORS = [
  { name: "Dr. Sneha Rao", department: "Cardiology" },
  { name: "Dr. Arjun Patel", department: "Orthopaedics" },
  { name: "Dr. Fatima Shaikh", department: "Paediatrics" },
  { name: "Dr. Vikram Nair", department: "Emergency" },
];

const SLOTS = ["09:30 AM", "10:30 AM", "11:15 AM", "01:30 PM", "03:00 PM"];

const BookAppointment = () => {
  const [department, setDepartment] = useState("");
  const [doctor, setDoctor] = useState("");
  const [slot, setSlot] = useState("");

  const doctors = useMemo(
    () => DOCTORS.filter((doc) => doc.department === department),
    [department]
  );

  const isConfirmed = department && doctor && slot;

  return (
    <div className="space-y-8">
      <Navbar title="Book Appointment" subtitle="Schedule Your Visit" />

      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-6">
        <div>
          <p className="text-sm text-slate-500">Step 1</p>
          <label className="text-sm font-semibold text-slate-700">Select department</label>
          <select
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm"
            value={department}
            onChange={(event) => {
              setDepartment(event.target.value);
              setDoctor("");
            }}
          >
            <option value="">Choose department</option>
            {DEPARTMENTS.map((dept) => (
              <option key={dept} value={dept}>
                {dept}
              </option>
            ))}
          </select>
        </div>

        <div>
          <p className="text-sm text-slate-500">Step 2</p>
          <label className="text-sm font-semibold text-slate-700">Select doctor</label>
          <select
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm"
            value={doctor}
            onChange={(event) => setDoctor(event.target.value)}
            disabled={!department}
          >
            <option value="">Choose doctor</option>
            {doctors.map((doc) => (
              <option key={doc.name} value={doc.name}>
                {doc.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <p className="text-sm text-slate-500">Step 3</p>
          <label className="text-sm font-semibold text-slate-700">Select time slot</label>
          <select
            className="mt-2 w-full border border-slate-200 rounded-xl px-3 py-2 text-sm"
            value={slot}
            onChange={(event) => setSlot(event.target.value)}
            disabled={!doctor}
          >
            <option value="">Choose slot</option>
            {SLOTS.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
        </div>
      </div>

      {isConfirmed && (
        <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6">
          <p className="text-sm uppercase tracking-[0.2em] text-blue-400">Confirmation</p>
          <h3 className="text-lg font-semibold text-slate-900 mt-2">Appointment scheduled</h3>
          <p className="text-sm text-slate-600 mt-2">
            {department} | {doctor} | {slot}
          </p>
        </div>
      )}
    </div>
  );
};

export default BookAppointment;
