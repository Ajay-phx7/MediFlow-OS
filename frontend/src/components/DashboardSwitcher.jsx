import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronDown, Check, LayoutDashboard, Stethoscope, UserRound } from "lucide-react";

const DashboardSwitcher = ({ currentRole, onRoleChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  const dashboards = [
    {
      id: "admin",
      label: "Admin Dashboard",
      icon: LayoutDashboard,
      path: "/admin/login",
    },
    {
      id: "doctor",
      label: "Doctor Dashboard",
      icon: Stethoscope,
      path: "/doctor/login",
    },
    {
      id: "patient",
      label: "Patient Dashboard",
      icon: UserRound,
      path: "/patient/login",
    },
  ];

  const currentDashboard = dashboards.find((d) => d.id === currentRole);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const handleRoleSelect = (dashboard) => {
    if (dashboard.id === currentRole) {
      setIsOpen(false);
      return;
    }

    setIsOpen(false);
    
    // Call the onRoleChange callback if provided
    if (onRoleChange) {
      onRoleChange(dashboard.id);
    } else {
      // Fallback navigation
      navigate(dashboard.path);
    }
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={toggleDropdown}
        className="flex items-center justify-between w-full px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 transition text-left group"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <div className="flex items-center gap-3 min-w-0">
          {currentDashboard && (
            <>
              <currentDashboard.icon className="h-4 w-4 text-cyan-400 flex-shrink-0" />
              <div className="hidden sm:block min-w-0">
                <p className="text-xs text-slate-400 uppercase tracking-wider">Dashboard</p>
                <p className="text-sm font-semibold text-white truncate">{currentDashboard.label}</p>
              </div>
            </>
          )}
        </div>
        <ChevronDown
          className={`h-4 w-4 text-slate-400 group-hover:text-slate-300 transition-transform duration-200 flex-shrink-0 ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-slate-800 rounded-xl shadow-lg border border-slate-700 overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
          {dashboards.map((dashboard) => {
            const Icon = dashboard.icon;
            const isActive = dashboard.id === currentRole;

            return (
              <button
                key={dashboard.id}
                onClick={() => handleRoleSelect(dashboard)}
                className={`flex items-center justify-between w-full px-3 py-3 transition ${
                  isActive
                    ? "bg-slate-700 text-white"
                    : "text-slate-300 hover:bg-slate-700 hover:text-white"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`h-4 w-4 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                  <span className="text-sm font-medium">{dashboard.label}</span>
                </div>
                {isActive && <Check className="h-4 w-4 text-cyan-400" />}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DashboardSwitcher;

// Made with Bob
