import { useContext, useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { getPatientHealthReport } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const HealthReport = () => {
  const [report, setReport] = useState(null);
  const { selectedPatient } = useContext(AppContext);

  useEffect(() => {
    if (!selectedPatient?.id) {
      return;
    }
    getPatientHealthReport(selectedPatient.id).then((response) => setReport(response.data));
  }, [selectedPatient]);

  return (
    <div className="space-y-8">
      <Navbar title="My Health Report" subtitle={selectedPatient?.name ?? "Summary & Labs"} />

      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">Patient Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-sm text-slate-600">
            <p>Name: {report?.summary?.name ?? "--"}</p>
            <p>DOB: {report?.summary?.dob ?? "--"}</p>
            <p>Blood Group: {report?.summary?.blood_group ?? "--"}</p>
            <p>Allergies: {report?.summary?.allergies ?? "--"}</p>
          </div>
        </div>

        <div>
          <h4 className="text-base font-semibold text-slate-900">Current Medications</h4>
          <ul className="mt-2 text-sm text-slate-600 list-disc list-inside">
            {report?.current_medications?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-base font-semibold text-slate-900">Past Diagnoses</h4>
          <ul className="mt-2 text-sm text-slate-600 list-disc list-inside">
            {report?.past_diagnoses?.map((item) => (
              <li key={item.diagnosis}>
                {item.diagnosis}{item.date ? ` (${item.date})` : ""}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-base font-semibold text-slate-900">Recent Lab Results</h4>
          <div className="mt-3 space-y-2 text-sm text-slate-600">
            {report?.recent_lab_results?.map((item) => (
              <div
                key={item.test}
                className="flex items-center justify-between bg-slate-50 rounded-xl px-3 py-2"
              >
                <span>{item.test}</span>
                <span>{item.value}</span>
                <span className="text-slate-400">{item.date}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-base font-semibold text-slate-900">Vaccinations</h4>
          <ul className="mt-2 text-sm text-slate-600 list-disc list-inside">
            {report?.vaccinations?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <button className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-semibold text-slate-600">
          Download PDF
        </button>
      </div>
    </div>
  );
};

export default HealthReport;
