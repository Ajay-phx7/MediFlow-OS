import { useContext, useEffect, useState } from "react";

import Badge from "../../components/Badge.jsx";
import Navbar from "../../components/Navbar.jsx";
import { getDoctorPatients } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientList = () => {
  const [patients, setPatients] = useState([]);
  const [activePatient, setActivePatient] = useState(null);
  const { selectedDoctor } = useContext(AppContext);

  useEffect(() => {
    getDoctorPatients(selectedDoctor?.id).then((response) => setPatients(response.data.patients));
  }, [selectedDoctor]);

  return (
    <div className="space-y-8">
      <Navbar title="My Patients" subtitle={selectedDoctor?.name ?? "Today's Schedule"} />

      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium">Age</th>
              <th className="px-4 py-3 font-medium">Appointment Time</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient) => {
              return (
                <tr key={patient.id} className="border-t border-slate-100">
                  <td className="px-4 py-3 font-medium text-slate-900">{patient.name}</td>
                  <td className="px-4 py-3 text-slate-600">{patient.age}</td>
                  <td className="px-4 py-3 text-slate-600">{patient.summary?.next_appointment ?? "--"}</td>
                  <td className="px-4 py-3">
                    <Badge label={patient.visit_history > 0 ? "Active" : "New"} tone={patient.visit_history > 0 ? "consultation" : "waiting"} />
                  </td>
                  <td className="px-4 py-3">
                    <button
                      className="text-xs font-semibold text-blue-600 hover:text-blue-700"
                      onClick={() => setActivePatient(patient)}
                    >
                      View Notes
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {activePatient && (
        <div className="fixed inset-0 bg-slate-900/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold text-slate-900">{activePatient.name}</h3>
            <p className="text-sm text-slate-500 mt-1">Recent history</p>
            <p className="text-sm text-slate-600 mt-3">Conditions: {activePatient.existing_conditions?.join(", ") || "None"}</p>
            <p className="text-sm text-slate-600 mt-2">Current medications: {activePatient.current_medications?.map((med) => med.name).join(", ") || "None"}</p>
            <p className="text-sm text-slate-600 mt-2">Latest SOAP note: {activePatient.latest_consultation?.soap_notes ?? "No consultation available"}</p>
            <button
              className="mt-6 px-4 py-2 rounded-xl bg-blue-600 text-white text-sm font-semibold"
              onClick={() => setActivePatient(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientList;
