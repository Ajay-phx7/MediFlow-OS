import { useContext, useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { getPatientDashboard } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientDashboard = () => {
  const [data, setData] = useState(null);
  const { selectedPatient } = useContext(AppContext);

  useEffect(() => {
    getPatientDashboard(selectedPatient?.id).then((response) => setData(response.data));
  }, [selectedPatient]);

  return (
    <div className="space-y-8">
      <Navbar title="Patient Dashboard" subtitle={selectedPatient?.name ?? "Welcome Back"} />

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
                <p className="text-sm text-slate-600 mt-2">{prescription.notes}</p>
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
                <p className="text-sm text-slate-600 mt-2 whitespace-pre-line">{consultation.soap_notes ?? consultation.notes}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
