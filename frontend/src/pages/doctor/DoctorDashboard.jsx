import { CalendarCheck, CheckCircle2, Clock, HeartPulse, NotebookText, UserRound } from "lucide-react";
import { useContext, useEffect, useState } from "react";

import { getDoctorDashboard, getDoctorPatients } from "../../api/index.js";
import Navbar from "../../components/Navbar.jsx";
import StatCard from "../../components/StatCard.jsx";
import { AppContext } from "../../context/AppContext.jsx";

const DoctorDashboard = () => {
  const [data, setData] = useState(null);
  const [patients, setPatients] = useState([]);
  const { selectedDoctor } = useContext(AppContext);

  useEffect(() => {
    const doctorId = selectedDoctor?.id;
    Promise.all([getDoctorDashboard(doctorId), getDoctorPatients(doctorId)]).then(([dashboardResponse, patientsResponse]) => {
      setData(dashboardResponse.data);
      setPatients(patientsResponse.data.patients ?? []);
    });
  }, [selectedDoctor]);

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
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">Next patient</p>
              <h3 className="text-xl font-semibold text-slate-900 mt-2">
                {data?.next_patient?.name ?? "No upcoming patient"}
              </h3>
              <p className="text-sm text-slate-600 mt-1">
                Age {data?.next_patient?.age ?? "--"} | {data?.next_patient?.complaint ?? "--"}
              </p>
            </div>
            <HeartPulse className="h-10 w-10 text-cyan-500" />
          </div>

          <div className="mt-6 space-y-3">
            {data?.today_appointments?.map((appointment) => (
              <div key={appointment.id} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-semibold text-slate-900">{appointment.patient}</p>
                    <p className="text-sm text-slate-600">{appointment.reason}</p>
                  </div>
                  <div className="text-right text-sm text-slate-500">
                    <p>{appointment.date}</p>
                    <p>{appointment.time}</p>
                  </div>
                </div>
                {appointment.notes ? <p className="text-sm text-slate-500 mt-2">{appointment.notes}</p> : null}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <div className="flex items-center gap-2">
            <UserRound className="h-5 w-5 text-cyan-600" />
            <h3 className="text-lg font-semibold text-slate-900">Assigned patients</h3>
          </div>
          <div className="mt-4 space-y-3 max-h-[34rem] overflow-auto pr-1">
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

                <div className="mt-3 space-y-2 text-sm text-slate-600 opacity-90">
                  <p>Blood group: {patient.blood_group ?? "--"}</p>
                  <p>Allergies: {patient.allergies ?? "--"}</p>
                  <p>Current medications: {patient.current_medications?.map((med) => med.name).join(", ") || "None"}</p>
                  <div className="rounded-xl bg-slate-50 p-3 text-slate-500 opacity-0 group-hover:opacity-100 transition">
                    <p className="font-medium text-slate-700">Hover details</p>
                    <p className="mt-1">Conditions: {patient.existing_conditions?.join(", ") || "None"}</p>
                    <p className="mt-1">Phone: {patient.phone ?? "--"}</p>
                    <p className="mt-1">Previous meds: {patient.previous_medications?.map((med) => med.name).join(", ") || "None"}</p>
                    <p className="mt-1">Latest note: {patient.latest_consultation?.soap_notes ?? "No consultation yet"}</p>
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
    </div>
  );
};

export default DoctorDashboard;
