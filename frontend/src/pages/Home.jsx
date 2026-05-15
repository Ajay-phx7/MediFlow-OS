import { Shield, Stethoscope, UserRound } from "lucide-react";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AppContext } from "../context/AppContext.jsx";

const ROLE_CARDS = [
  {
    title: "Admin / Reception",
    description: "Oversee queues, departments, and surge forecasts.",
    icon: Shield,
    to: "/admin",
    role: "admin",
  },
  {
    title: "Doctor",
    description: "Review patients, document visits, and create notes.",
    icon: Stethoscope,
    to: "/doctor",
    role: "doctor",
  },
  {
    title: "Patient",
    description: "Track appointments, congestion, and health report.",
    icon: UserRound,
    to: "/patient",
    role: "patient",
  },
];

const Home = () => {
  const navigate = useNavigate();
  const { setActiveRole } = useContext(AppContext);

  const handleSelect = (role, path) => {
    setActiveRole(role);
    navigate(path);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 relative overflow-hidden">
      <div className="absolute -top-20 -right-20 h-64 w-64 rounded-full bg-blue-100 blur-3xl" />
      <div className="absolute bottom-10 left-10 h-56 w-56 rounded-full bg-amber-100 blur-3xl" />

      <div className="relative z-10 max-w-5xl mx-auto px-6 py-16">
        <div className="text-center">
          <p className="text-xs uppercase tracking-[0.4em] text-slate-400">Hospital Management Platform</p>
          <h1 className="text-4xl sm:text-5xl font-semibold text-slate-900 mt-4">MediCore</h1>
          <p className="text-base sm:text-lg text-slate-600 mt-4">
            Choose your role to explore the hospital operations dashboard.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          {ROLE_CARDS.map((card) => {
            const Icon = card.icon;
            return (
              <button
                key={card.title}
                className="text-left bg-white border border-slate-200 rounded-3xl p-6 shadow-sm hover:shadow-md transition"
                onClick={() => handleSelect(card.role, card.to)}
              >
                <div className="h-12 w-12 rounded-2xl bg-blue-600 text-white flex items-center justify-center">
                  <Icon className="h-6 w-6" />
                </div>
                <h2 className="text-xl font-semibold text-slate-900 mt-4">{card.title}</h2>
                <p className="text-sm text-slate-500 mt-2">{card.description}</p>
                <div className="mt-6 text-sm font-semibold text-blue-600">Enter workspace</div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Home;
