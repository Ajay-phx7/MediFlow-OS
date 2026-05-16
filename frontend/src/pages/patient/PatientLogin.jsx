import { useContext, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getAvailablePatients, loginAsPatient } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientLogin = () => {
  const navigate = useNavigate();
  const { setSelectedPatient } = useContext(AppContext);
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    getAvailablePatients().then((response) => {
      setPatients(response.data);
      setSelectedId(response.data[0]?.id ?? null);
    });
  }, []);

  const filteredPatients = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return patients;

    return patients.filter((patient) => patient.name.toLowerCase().includes(term));
  }, [patients, search]);

  const selectedPatient = useMemo(
    () => filteredPatients.find((patient) => patient.id === Number(selectedId)),
    [filteredPatients, selectedId]
  );

  useEffect(() => {
    if (!selectedPatient && filteredPatients.length > 0) {
      setSelectedId(filteredPatients[0].id);
    }
  }, [filteredPatients, selectedPatient]);

  const handleContinue = async () => {
    if (!selectedPatient) return;

    setIsLoading(true);
    try {
      const response = await loginAsPatient(selectedPatient.id);
      setSelectedPatient(response.data.patient);
      navigate("/patient");
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
        <div className="max-w-5xl w-full grid gap-gutter lg:grid-cols-[0.95fr_1.05fr]">
          {/* Patient Selection Panel */}
          <div className="glass-panel p-8 rounded-xl">
            <p className="font-data-label text-data-label text-primary-container uppercase tracking-wider">
              Patient Access
            </p>
            <h1 className="font-headline-lg text-headline-lg text-primary mt-4">
              Search and select your profile
            </h1>
            <p className="text-on-surface-variant mt-4 leading-relaxed">
              No password is needed. Pick your patient record, and the dashboard will show only your appointments, prescriptions, and consultation history.
            </p>

            <div className="relative mt-8">
              <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant">
                search
              </span>
              <input
                className="w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 pl-12 pr-4 text-on-surface placeholder:text-on-surface-variant/50 outline-none focus:border-primary-container focus:shadow-glow-cyan transition-all"
                placeholder="Search patient name"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>

            <div className="grid gap-3 mt-6 max-h-[34rem] overflow-auto pr-1">
              {filteredPatients.map((patient) => (
                <button
                  key={patient.id}
                  className={`text-left rounded-xl border p-4 transition-all duration-300 ${
                    selectedId === patient.id
                      ? "border-primary-container bg-primary-container/10 shadow-glow-cyan"
                      : "border-outline-variant bg-surface-container-low hover:border-primary-container/50"
                  }`}
                  onClick={() => setSelectedId(patient.id)}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-headline-lg font-semibold text-primary">
                        {patient.name}
                      </p>
                      <p className="text-sm text-on-surface-variant mt-1">
                        Age {patient.age ?? "--"} • Blood group {patient.blood_group ?? "--"}
                      </p>
                    </div>
                    <span className="font-data-label text-xs uppercase tracking-wider text-primary-container">
                      #{patient.id}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Preview Panel */}
          <div className="glass-panel p-8 rounded-xl">
            <p className="font-data-label text-data-label text-on-surface-variant uppercase tracking-wider">
              Preview
            </p>
            <div className="mt-6 rounded-xl bg-gradient-to-br from-primary-container/20 to-secondary-container/10 border border-primary-container/30 p-6">
              <p className="text-sm text-on-surface-variant">Selected patient</p>
              <h2 className="font-headline-lg text-2xl font-semibold text-primary mt-2">
                {selectedPatient?.name ?? "Select a patient"}
              </h2>
              <p className="text-on-surface-variant mt-1">
                {selectedPatient
                  ? `Age ${selectedPatient.age ?? "--"} • ${selectedPatient.blood_group ?? "--"}`
                  : "Your personal records will appear here."}
              </p>
            </div>

            <button
              className="mt-6 w-full rounded-xl bg-primary-container text-on-primary-container py-3.5 font-bold disabled:opacity-50 hover:scale-105 transition-transform duration-150 active:scale-95"
              disabled={!selectedPatient || isLoading}
              onClick={handleContinue}
            >
              {isLoading ? "Opening dashboard..." : "Open patient dashboard"}
            </button>

            <p className="text-xs text-on-surface-variant mt-4 leading-relaxed">
              The search list is filtered locally and the chosen patient is stored so follow-up views stay on the same record across refreshes.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PatientLogin;

// Made with Bob
