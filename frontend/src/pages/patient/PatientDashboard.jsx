import { useContext, useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { getPatientDashboard } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientDashboard = () => {
  const [data, setData] = useState(null);
  const { selectedPatient } = useContext(AppContext);

  useEffect(() => {
    if (!selectedPatient?.id) {
      return;
    }
    getPatientDashboard(selectedPatient.id).then((response) => setData(response.data));
  }, [selectedPatient]);

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
