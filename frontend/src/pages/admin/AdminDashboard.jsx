import { BedDouble, Timer, Users, AlertTriangle } from "lucide-react";
import { useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import StatCard from "../../components/StatCard.jsx";
import { getAdminStats } from "../../api/index.js";

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getAdminStats().then((response) => setStats(response.data));
  }, []);

  return (
    <div className="space-y-8">
      <Navbar title="Admin Dashboard" subtitle="Operational Overview" />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard
          label="Total patients today"
          value={stats?.total_patients_today ?? "--"}
          icon={Users}
        />
        <StatCard
          label="Avg wait time"
          value={stats ? `${stats.avg_wait_time_min} min` : "--"}
          icon={Timer}
          accent="text-amber-600"
        />
        <StatCard
          label="Beds available"
          value={stats?.beds_available ?? "--"}
          icon={BedDouble}
          accent="text-green-600"
        />
        <StatCard
          label="Departments on alert"
          value={stats?.departments_on_alert ?? "--"}
          icon={AlertTriangle}
          accent="text-red-600"
        />
      </div>
    </div>
  );
};

export default AdminDashboard;
