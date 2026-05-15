import { useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { getPatientDashboard } from "../../api/index.js";

const PatientDashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getPatientDashboard().then((response) => setData(response.data));
  }, []);

  return (
    <div className="space-y-8">
      <Navbar title="Patient Dashboard" subtitle="Welcome Back" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Hello, {data?.name ?? "--"}</h3>
          <p className="text-sm text-slate-600 mt-2">Here is your upcoming appointment.</p>
          <div className="mt-4 bg-slate-50 rounded-xl p-4">
            <p className="text-sm text-slate-500">Doctor</p>
            <p className="text-base font-semibold text-slate-900">
              {data?.upcoming_appointment?.doctor ?? "--"}
            </p>
            <p className="text-sm text-slate-600 mt-1">
              {data?.upcoming_appointment?.department ?? "--"} | {data?.upcoming_appointment?.time ?? "--"}
            </p>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-900">Current medications</h3>
          <ul className="mt-4 space-y-2">
            {data?.medications?.map((item) => (
              <li key={item} className="text-sm text-slate-600">
                - {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
