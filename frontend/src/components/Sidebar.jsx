import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { getEmergencyAlerts } from "../api/index.js";
import DashboardSwitcher from "./DashboardSwitcher.jsx";

const Sidebar = ({ items, title, currentRole, onRoleChange }) => {
  const [criticalCount, setCriticalCount] = useState(0);

  useEffect(() => {
    // Only fetch alerts for admin sidebar
    if (title === "Admin / Reception") {
      fetchCriticalAlerts();
      // Refresh every 30 seconds
      const interval = setInterval(fetchCriticalAlerts, 30000);
      return () => clearInterval(interval);
    }
  }, [title]);

  const fetchCriticalAlerts = async () => {
    try {
      const response = await getEmergencyAlerts();
      const critical = response.data.filter(
        (alert) => alert.severity === "Critical"
      ).length;
      setCriticalCount(critical);
    } catch (error) {
      console.error("Error fetching critical alerts:", error);
    }
  };
  return (
    <aside className="bg-slate-900 text-slate-100 sm:w-64 w-16 min-h-screen flex flex-col">
      <div className="px-4 py-6 border-b border-slate-800 space-y-4">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold">
            M
          </div>
          <div className="hidden sm:block">
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">MediFlow-OS</p>
          </div>
        </div>
        {currentRole && onRoleChange && (
          <DashboardSwitcher currentRole={currentRole} onRoleChange={onRoleChange} />
        )}
      </div>
      <nav className="flex-1 px-2 py-6 space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          const isEmergency = item.label === "Emergency";
          const showBadge = isEmergency && criticalCount > 0;

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 px-3 py-3 rounded-xl transition relative",
                  isActive
                    ? "bg-slate-800 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white",
                ].join(" ")
              }
              end={item.end}
            >
              <div className="relative">
                <Icon className="h-5 w-5" />
                {showBadge && (
                  <div className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-[10px] font-bold">
                      {criticalCount}
                    </span>
                  </div>
                )}
              </div>
              <span className="hidden sm:inline text-sm font-medium">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
      <div className="px-4 py-4 text-xs text-slate-500 hidden sm:block">
        Prototype v0.1
      </div>
    </aside>
  );
};

export default Sidebar;
