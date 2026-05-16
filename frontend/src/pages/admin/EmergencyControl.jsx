import { useEffect, useState } from "react";
import { AlertTriangle, Truck, UserCheck } from "lucide-react";

import Navbar from "../../components/Navbar.jsx";
import {
  getEmergencyAlerts,
  getEmergencyResources,
  escalateAlert,
  getProtocol,
} from "../../api/index.js";

const EmergencyControl = () => {
  const [alerts, setAlerts] = useState([]);
  const [resources, setResources] = useState(null);
  const [selectedProtocol, setSelectedProtocol] = useState("Cardiac Arrest");
  const [protocolData, setProtocolData] = useState(null);
  const [checkedSteps, setCheckedSteps] = useState({});

  useEffect(() => {
    fetchAlerts();
    fetchResources();
    fetchProtocol("Cardiac Arrest");
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await getEmergencyAlerts();
      setAlerts(response.data);
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  };

  const fetchResources = async () => {
    try {
      const response = await getEmergencyResources();
      setResources(response.data);
    } catch (error) {
      console.error("Error fetching resources:", error);
    }
  };

  const fetchProtocol = async (type) => {
    try {
      const response = await getProtocol(type);
      setProtocolData(response.data);
      setCheckedSteps({});
    } catch (error) {
      console.error("Error fetching protocol:", error);
    }
  };

  const handleEscalate = async (alertId, level) => {
    try {
      await escalateAlert(alertId, level);
      setAlerts((prev) =>
        prev.map((alert) =>
          alert.id === alertId ? { ...alert, escalated: true } : alert
        )
      );
    } catch (error) {
      console.error("Error escalating alert:", error);
    }
  };

  const handleProtocolChange = (type) => {
    setSelectedProtocol(type);
    fetchProtocol(type);
  };

  const toggleStep = (index) => {
    setCheckedSteps((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const resetChecklist = () => {
    setCheckedSteps({});
  };

  const hasCriticalAlert = alerts.some((alert) => alert.severity === "Critical");
  const completedSteps = protocolData
    ? Object.values(checkedSteps).filter(Boolean).length
    : 0;
  const totalSteps = protocolData?.steps?.length || 0;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "Critical":
        return "border-red-500";
      case "High":
        return "border-amber-500";
      case "Moderate":
        return "border-yellow-500";
      default:
        return "border-slate-300";
    }
  };

  const getSeverityBadgeColor = (severity) => {
    switch (severity) {
      case "Critical":
        return "bg-red-100 text-red-800";
      case "High":
        return "bg-amber-100 text-amber-800";
      case "Moderate":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-slate-100 text-slate-800";
    }
  };

  const getAmbulanceColor = (status) => {
    switch (status) {
      case "available":
        return "bg-green-100 text-green-800";
      case "en-route":
        return "bg-amber-100 text-amber-800";
      case "maintenance":
        return "bg-slate-200 text-slate-600";
      default:
        return "bg-slate-100 text-slate-800";
    }
  };

  const getBedOccupancyColor = (occupancy) => {
    if (occupancy < 0.5) return "bg-green-500";
    if (occupancy <= 0.8) return "bg-amber-500";
    return "bg-red-500";
  };

  const bedOccupancy = resources
    ? (resources.er_beds.total - resources.er_beds.free) / resources.er_beds.total
    : 0;

  return (
    <div className="space-y-8">
      <Navbar title="Emergency Control" subtitle="Real-time Crisis Management" />

      {/* PANEL 1 - Live Alert Feed */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Live Alert Feed</h2>

        {hasCriticalAlert && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-4 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span className="font-medium">
              ⚠ Critical alert active — immediate action required
            </span>
          </div>
        )}

        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`border-l-4 ${getSeverityColor(
                alert.severity
              )} bg-slate-50 rounded-lg p-4`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    {alert.severity === "Critical" && (
                      <div className="h-3 w-3 bg-red-500 rounded-full animate-pulse" />
                    )}
                    <h3 className="font-semibold text-lg">{alert.type}</h3>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadgeColor(
                        alert.severity
                      )}`}
                    >
                      {alert.severity}
                    </span>
                  </div>
                  <p className="text-slate-600 text-sm mb-1">
                    <span className="font-medium">Location:</span> {alert.location}
                  </p>
                  <p className="text-slate-500 text-sm">{alert.elapsed}</p>
                  {alert.note && (
                    <p className="text-slate-600 italic text-sm mt-2">{alert.note}</p>
                  )}
                </div>
                <div>
                  {alert.escalated ? (
                    <div className="text-green-600 font-medium text-sm">
                      Escalated ✓
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEscalate(alert.id, alert.severity)}
                      className="px-4 py-2 border-2 border-red-500 text-red-600 rounded-lg text-sm font-medium hover:bg-red-50 transition"
                    >
                      Escalate
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* PANEL 2 - Resource Status Board */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-6">Resource Status Board</h2>

        {resources && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Ambulances */}
            <div>
              <h3 className="font-semibold mb-3 text-slate-700">Ambulances</h3>
              <div className="grid grid-cols-3 gap-3">
                {resources.ambulances.map((ambulance) => (
                  <div
                    key={ambulance.id}
                    className={`${getAmbulanceColor(
                      ambulance.status
                    )} rounded-lg p-3 flex flex-col items-center justify-center`}
                  >
                    <Truck className="h-6 w-6 mb-2" />
                    <span className="text-xs font-medium">{ambulance.id}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* ER Beds */}
            <div>
              <h3 className="font-semibold mb-3 text-slate-700">ER Beds</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-slate-600 mb-1">
                  <span>
                    {resources.er_beds.free} free / {resources.er_beds.total} total
                  </span>
                  <span>{Math.round(bedOccupancy * 100)}% occupied</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-4 overflow-hidden">
                  <div
                    className={`h-full ${getBedOccupancyColor(
                      bedOccupancy
                    )} transition-all`}
                    style={{ width: `${bedOccupancy * 100}%` }}
                  />
                </div>
              </div>
            </div>

            {/* On-call Surgeons */}
            <div>
              <h3 className="font-semibold mb-3 text-slate-700">On-call Surgeons</h3>
              <div className="flex items-center gap-3 bg-blue-50 rounded-lg p-4">
                <UserCheck className="h-8 w-8 text-blue-600" />
                <span className="text-2xl font-bold text-blue-900">
                  {resources.on_call_surgeons}
                </span>
              </div>
            </div>

            {/* Blood Bank */}
            <div>
              <h3 className="font-semibold mb-3 text-slate-700">Blood Bank</h3>
              <div className="flex flex-wrap gap-2">
                {resources.blood_bank.map((blood) => (
                  <div
                    key={blood.type}
                    className={`px-4 py-2 rounded-full text-sm font-medium ${
                      blood.status === "low"
                        ? "bg-red-100 text-red-800"
                        : "bg-green-100 text-green-800"
                    }`}
                  >
                    {blood.type}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* PANEL 3 - Emergency Protocol Viewer */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-4">Emergency Protocol Viewer</h2>

        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Select Protocol
          </label>
          <select
            value={selectedProtocol}
            onChange={(e) => handleProtocolChange(e.target.value)}
            className="w-full md:w-auto px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Cardiac Arrest">Cardiac Arrest</option>
            <option value="Trauma">Trauma</option>
            <option value="Fire">Fire</option>
            <option value="Mass Casualty">Mass Casualty</option>
          </select>
        </div>

        {protocolData && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm text-slate-600">
                <span className="font-semibold text-blue-600">{completedSteps}</span> /{" "}
                {totalSteps} steps completed
              </div>
              <button
                onClick={resetChecklist}
                className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 transition"
              >
                Reset Checklist
              </button>
            </div>

            <div className="space-y-3">
              {protocolData.steps.map((step, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition"
                >
                  <input
                    type="checkbox"
                    checked={checkedSteps[index] || false}
                    onChange={() => toggleStep(index)}
                    className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
                  />
                  <label
                    onClick={() => toggleStep(index)}
                    className={`flex-1 cursor-pointer ${
                      checkedSteps[index]
                        ? "line-through text-green-600"
                        : "text-slate-700"
                    }`}
                  >
                    <span className="font-medium mr-2">{index + 1}.</span>
                    {step}
                  </label>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmergencyControl;

// Made with Bob
