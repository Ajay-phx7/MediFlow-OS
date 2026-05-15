import { CalendarCheck, CheckCircle2, Clock } from "lucide-react";
import { useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import StatCard from "../../components/StatCard.jsx";
import { getDoctorDashboard } from "../../api/index.js";

const DoctorDashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getDoctorDashboard().then((response) => setData(response.data));
  }, []);

  return (
    <div className="space-y-8">
      <Navbar title="Doctor Dashboard" subtitle="Daily Overview" />

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

      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <p className="text-sm text-slate-500">Next patient</p>
        <h3 className="text-xl font-semibold text-slate-900 mt-2">
          {data?.next_patient?.name ?? "--"}
        </h3>
        <p className="text-sm text-slate-600 mt-1">
          Age {data?.next_patient?.age ?? "--"} | {data?.next_patient?.complaint ?? "--"}
        </p>
      </div>
    </div>
  );
};

export default DoctorDashboard;
