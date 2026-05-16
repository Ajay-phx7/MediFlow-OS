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
    <aside className="glass-panel sm:w-64 w-16 min-h-screen flex flex-col border-r border-outline-variant/30">
      <div className="px-4 py-6 border-b border-outline-variant/30 space-y-4">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-primary-container text-on-primary-container flex items-center justify-center font-bold">
            M
          </div>
          <div className="hidden sm:block">
            <p className="font-data-label text-xs uppercase tracking-wider text-primary-container">
              MediFlow-OS
            </p>
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
                  "flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-300 relative",
                  isActive
                    ? "bg-primary-container/20 text-primary border border-primary-container/40 shadow-glow-cyan"
                    : "text-on-surface-variant hover:bg-surface-container-high hover:text-primary hover:border hover:border-primary-container/20",
                ].join(" ")
              }
              end={item.end}
            >
              <div className="relative">
                <Icon className="h-5 w-5" />
                {showBadge && (
                  <div className="absolute -top-1 -right-1 h-4 w-4 bg-error rounded-full flex items-center justify-center animate-pulse">
                    <span className="text-on-error text-[10px] font-bold">
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
      
      <div className="px-4 py-4 border-t border-outline-variant/30 hidden sm:block">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-primary-container animate-pulse shadow-glow-cyan"></div>
          <span className="font-data-label text-xs text-on-surface-variant">
            System Active
          </span>
        </div>
        <p className="font-data-label text-[10px] text-on-surface-variant/60 mt-2 tracking-wider">
          PROTOTYPE v0.1
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;

// Made with Bob
