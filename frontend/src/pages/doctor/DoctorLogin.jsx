import { useContext, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getAvailableDoctors, loginAsDoctor } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const DoctorLogin = () => {
  const navigate = useNavigate();
  const { setSelectedDoctor } = useContext(AppContext);
  const [doctors, setDoctors] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    getAvailableDoctors().then((response) => {
      setDoctors(response.data);
      setSelectedId(response.data[0]?.id ?? null);
    });
  }, []);

  const selectedDoctor = useMemo(
    () => doctors.find((doctor) => doctor.id === Number(selectedId)),
    [doctors, selectedId]
  );

  const handleContinue = async () => {
    if (!selectedDoctor) return;

    setIsLoading(true);
    try {
      const response = await loginAsDoctor(selectedDoctor.id);
      setSelectedDoctor(response.data.doctor);
      navigate("/doctor");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white flex items-center justify-center px-6 py-12">
      <div className="max-w-4xl w-full grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-[2rem] border border-white/10 bg-white/5 backdrop-blur p-8 shadow-2xl shadow-slate-950/30">
          <p className="text-xs uppercase tracking-[0.4em] text-cyan-300/80">Doctor access</p>
          <h1 className="text-4xl font-semibold mt-4">Choose a doctor profile</h1>
          <p className="text-slate-300 mt-4 max-w-xl">
            No password is required. Select a doctor to open the matching dashboard with only that doctor’s connected patients, appointments, and prescriptions.
          </p>

          <div className="grid gap-3 mt-8">
            {doctors.map((doctor) => (
              <button
                key={doctor.id}
                className={`text-left rounded-2xl border p-4 transition ${selectedId === doctor.id ? "border-cyan-400 bg-cyan-400/10" : "border-white/10 bg-white/5 hover:bg-white/10"}`}
                onClick={() => setSelectedId(doctor.id)}
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-lg font-semibold">{doctor.name}</p>
                    <p className="text-sm text-slate-300 mt-1">
                      {doctor.department} {doctor.specialization ? `• ${doctor.specialization}` : ""}
                    </p>
                  </div>
                  <span className="text-xs uppercase tracking-[0.25em] text-cyan-300">#{doctor.id}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-[2rem] border border-white/10 bg-slate-950/70 p-8 shadow-2xl shadow-slate-950/30">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Preview</p>
          <div className="mt-4 rounded-3xl bg-gradient-to-br from-cyan-500/20 to-blue-500/10 border border-white/10 p-6">
            <p className="text-sm text-slate-300">Selected doctor</p>
            <h2 className="text-2xl font-semibold mt-2">{selectedDoctor?.name ?? "Select a doctor"}</h2>
            <p className="text-slate-300 mt-1">{selectedDoctor?.department ?? "Department will appear here"}</p>
          </div>

          <button
            className="mt-6 w-full rounded-2xl bg-cyan-400 text-slate-950 py-3.5 font-semibold disabled:opacity-50"
            disabled={!selectedDoctor || isLoading}
            onClick={handleContinue}
          >
            {isLoading ? "Opening dashboard..." : "Open doctor dashboard"}
          </button>

          <p className="text-xs text-slate-400 mt-4 leading-6">
            This selection is stored locally so the dashboard and patient workspace stay aligned to the same connected mock record set.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DoctorLogin;