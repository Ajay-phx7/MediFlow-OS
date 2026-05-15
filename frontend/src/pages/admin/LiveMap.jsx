import { useEffect, useState } from "react";

import Badge from "../../components/Badge.jsx";
import Navbar from "../../components/Navbar.jsx";
import { getAdminLiveMap } from "../../api/index.js";

const LiveMap = () => {
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    getAdminLiveMap().then((response) => setDepartments(response.data.departments));
  }, []);

  return (
    <div className="space-y-8">
      <Navbar title="Live Map" subtitle="Department Congestion" />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {departments.map((dept) => (
          <div
            key={dept.name}
            className="bg-white border border-slate-200 rounded-2xl p-5"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-slate-900">{dept.name}</h3>
              <Badge label={dept.congestion} tone={dept.congestion.toLowerCase()} />
            </div>
            <p className="text-sm text-slate-500 mt-3">Current patients</p>
            <p className="text-3xl font-semibold text-slate-900 mt-1">{dept.patients}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LiveMap;
