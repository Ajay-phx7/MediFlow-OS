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
    <div className="min-h-screen flex flex-col overflow-x-hidden font-body-md text-body-md bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 flex justify-between items-center w-full px-margin-desktop py-4 bg-surface-bright border-b border-white/5">
        <div className="font-display-lg text-[24px] font-bold text-primary tracking-tighter">
          MediFlow OS
        </div>
        <button
          onClick={() => navigate("/")}
          className="text-on-surface-variant hover:text-surface-tint transition-colors text-sm"
        >
          ← Back to Home
        </button>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-6 py-12">
        <div className="max-w-5xl w-full grid gap-gutter lg:grid-cols-[1.1fr_0.9fr]">
          {/* Info Panel */}
          <div className="glass-panel p-8 rounded-xl">
            <p className="font-data-label text-data-label text-primary-container uppercase tracking-wider">
              Admin Access
            </p>
            <h1 className="font-headline-lg text-headline-lg text-primary mt-4">
              Admin / Reception Dashboard
            </h1>
            <p className="text-on-surface-variant mt-4 leading-relaxed">
              Access the administrative dashboard to manage hospital operations, monitor queues, track surge predictions, and coordinate emergency responses.
            </p>

            <div className="mt-8 glass-panel p-6 rounded-xl border-primary-container/20">
              <h3 className="font-headline-lg text-lg font-semibold text-primary mb-4">
                Dashboard Features
              </h3>
              <ul className="space-y-3 text-sm text-on-surface-variant">
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Operational overview and statistics</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Queue management system</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Surge prediction and forecasting</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Live resource monitoring</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Department communication</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary-container text-base">
                    check_circle
                  </span>
                  <span>Emergency control center</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Selection Panel */}
          <div className="glass-panel p-8 rounded-xl">
            <p className="font-data-label text-data-label text-on-surface-variant uppercase tracking-wider">
              Select Department
            </p>
            
            <label className="mt-6 block text-sm text-on-surface-variant">Admin account</label>
            <select
              className="mt-3 w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-3 text-on-surface outline-none focus:border-primary-container focus:shadow-glow-cyan transition-all"
              value={selectedAdminId ?? ""}
              onChange={(event) => setSelectedAdminId(Number(event.target.value))}
            >
              <option value="" disabled>
                Select an admin account
              </option>
              {admins.map((admin) => (
                <option key={admin.id} value={admin.id}>
                  {admin.department} - {admin.username}
                </option>
              ))}
            </select>

            <button
              className="mt-6 w-full rounded-xl bg-primary-container text-on-primary-container py-3.5 font-bold disabled:opacity-50 hover:scale-105 transition-transform duration-150 active:scale-95"
              disabled={isLoading || !selectedAdminId}
              onClick={handleContinue}
            >
              {isLoading ? "Opening dashboard..." : "Open admin dashboard"}
            </button>

            <p className="text-xs text-on-surface-variant mt-4 leading-relaxed">
              Select your department to access the administrative dashboard. All departments have full system access with personalized chat channels.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminLogin;

// Made with Bob
