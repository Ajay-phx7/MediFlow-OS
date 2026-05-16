import { Search } from "lucide-react";
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#f8fafc_0%,_#e2e8f0_45%,_#cbd5e1_100%)] text-slate-900 px-6 py-12">
      <div className="max-w-5xl mx-auto grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="rounded-[2rem] bg-slate-950 text-white p-8 shadow-2xl shadow-slate-400/20">
          <p className="text-xs uppercase tracking-[0.4em] text-cyan-300/80">Patient access</p>
          <h1 className="text-4xl font-semibold mt-4">Search and select your profile</h1>
          <p className="text-slate-300 mt-4 leading-7">
            No password is needed. Pick your patient record, and the dashboard will show only your appointments, prescriptions, and consultation history.
          </p>

          <div className="relative mt-8">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
            <input
              className="w-full rounded-2xl border border-white/10 bg-white/5 py-3 pl-12 pr-4 text-white placeholder:text-slate-500 outline-none focus:border-cyan-300"
              placeholder="Search patient name"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <div className="grid gap-3 mt-6 max-h-[34rem] overflow-auto pr-1">
            {filteredPatients.map((patient) => (
              <button
                key={patient.id}
                className={`text-left rounded-2xl border p-4 transition ${selectedId === patient.id ? "border-cyan-300 bg-cyan-300/10" : "border-white/10 bg-white/5 hover:bg-white/10"}`}
                onClick={() => setSelectedId(patient.id)}
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-semibold">{patient.name}</p>
                    <p className="text-sm text-slate-300 mt-1">
                      Age {patient.age ?? "--"} • Blood group {patient.blood_group ?? "--"}
                    </p>
                  </div>
                  <span className="text-xs uppercase tracking-[0.25em] text-cyan-300">#{patient.id}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-[2rem] bg-white/85 backdrop-blur p-8 shadow-2xl shadow-slate-400/20 border border-slate-200/70">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Preview</p>
          <div className="mt-4 rounded-3xl bg-gradient-to-br from-slate-900 to-slate-700 text-white p-6">
            <p className="text-sm text-slate-300">Selected patient</p>
            <h2 className="text-2xl font-semibold mt-2">{selectedPatient?.name ?? "Select a patient"}</h2>
            <p className="text-slate-300 mt-1">{selectedPatient ? `Age ${selectedPatient.age ?? "--"} • ${selectedPatient.blood_group ?? "--"}` : "Your personal records will appear here."}</p>
          </div>

          <button
            className="mt-6 w-full rounded-2xl bg-slate-950 text-white py-3.5 font-semibold disabled:opacity-50"
            disabled={!selectedPatient || isLoading}
            onClick={handleContinue}
          >
            {isLoading ? "Opening dashboard..." : "Open patient dashboard"}
          </button>

          <p className="text-xs text-slate-500 mt-4 leading-6">
            The search list is filtered locally and the chosen patient is stored so follow-up views stay on the same record across refreshes.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PatientLogin;