import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { AppContext } from "../../context/AppContext.jsx";
import { getAvailableAdmins, loginAsAdmin } from "../../api/index.js";

const AdminLogin = () => {
  const navigate = useNavigate();
  const { setSelectedAdmin } = useContext(AppContext);
  const [isLoading, setIsLoading] = useState(false);
  const [admins, setAdmins] = useState([]);
  const [selectedAdminId, setSelectedAdminId] = useState(null);

  useEffect(() => {
    // Fetch available admin accounts
    getAvailableAdmins()
      .then((response) => {
        setAdmins(response.data);
        if (response.data.length > 0) {
          setSelectedAdminId(response.data[0].id);
        }
      })
      .catch((error) => {
        console.error("Failed to fetch admin accounts:", error);
      });
  }, []);

  const handleContinue = async () => {
    if (!selectedAdminId) return;
    
    setIsLoading(true);
    try {
      const response = await loginAsAdmin(selectedAdminId);
      if (response.data.success) {
        setSelectedAdmin(response.data.admin);
        navigate("/admin");
      }
    } catch (error) {
      console.error("Login failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white flex items-center justify-center px-6 py-12">
      <div className="max-w-4xl w-full grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur p-8 shadow-2xl shadow-slate-950/30">
          <p className="text-xs uppercase tracking-[0.4em] text-cyan-300/80">Admin access</p>
          <h1 className="text-4xl font-semibold mt-4">Admin / Reception Dashboard</h1>
          <p className="text-slate-300 mt-4 max-w-xl">
            Access the administrative dashboard to manage hospital operations, monitor queues, track surge predictions, and coordinate emergency responses.
          </p>

          <div className="mt-8 space-y-4">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <h3 className="text-lg font-semibold mb-3">Dashboard Features</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Operational overview and statistics
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Queue management system
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Surge prediction and forecasting
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Live resource monitoring
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Department communication
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  Emergency control center
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="rounded-[2rem] border border-white/10 bg-slate-950/70 p-8 shadow-2xl shadow-slate-950/30">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Select Department</p>
          
          <div className="mt-4 space-y-4">
            {admins.map((admin) => (
              <button
                key={admin.id}
                className={`w-full text-left rounded-2xl border p-4 transition ${
                  selectedAdminId === admin.id
                    ? "border-cyan-400 bg-gradient-to-br from-cyan-500/20 to-blue-500/10"
                    : "border-white/10 bg-white/5 hover:border-white/20"
                }`}
                onClick={() => setSelectedAdminId(admin.id)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{admin.department}</h3>
                    <p className="text-sm text-slate-400 mt-1">{admin.username}</p>
                  </div>
                  {selectedAdminId === admin.id && (
                    <div className="h-3 w-3 rounded-full bg-cyan-400"></div>
                  )}
                </div>
              </button>
            ))}
          </div>

          <button
            className="mt-6 w-full rounded-2xl bg-cyan-400 text-slate-950 py-3.5 font-semibold disabled:opacity-50 hover:bg-cyan-300 transition"
            disabled={isLoading || !selectedAdminId}
            onClick={handleContinue}
          >
            {isLoading ? "Opening dashboard..." : "Open admin dashboard"}
          </button>

          <p className="text-xs text-slate-400 mt-4 leading-6">
            Select your department to access the administrative dashboard. All departments have full system access with personalized chat channels.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;

// Made with Bob
