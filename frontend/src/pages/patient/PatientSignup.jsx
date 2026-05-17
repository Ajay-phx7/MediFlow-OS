import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";

import { signupPatient } from "../../api/index.js";
import { AppContext } from "../../context/AppContext.jsx";

const PatientSignup = () => {
  const navigate = useNavigate();
  const { setSelectedPatient } = useContext(AppContext);
  const [form, setForm] = useState({
    name: "",
    date_of_birth: "",
    age: "",
    blood_group: "",
    allergies: "",
    phone: "",
    email: "",
    address: "",
  });
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      const payload = {
        ...form,
        age: Number(form.age),
      };
      const response = await signupPatient(payload);
      if (response.data.error) {
        setError(response.data.error);
        return;
      }
      setMessage(response.data.message ?? "Profile created.");
      if (response.data.patient) {
        setSelectedPatient(response.data.patient);
        navigate("/patient");
      }
    } catch (err) {
      console.error("Signup failed:", err);
      setError(err.response?.data?.error || "Failed to create profile.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col overflow-x-hidden font-body-md text-body-md bg-background">
      <header className="sticky top-0 z-50 flex justify-between items-center w-full px-margin-desktop py-4 bg-surface-bright border-b border-white/5">
        <div className="font-display-lg text-[24px] font-bold text-primary tracking-tighter">
          MediFlow OS
        </div>
        <button
          onClick={() => navigate("/patient/login")}
          className="text-on-surface-variant hover:text-surface-tint transition-colors text-sm"
        >
          ← Back to patient login
        </button>
      </header>

      <main className="flex-grow flex items-center justify-center px-6 py-12">
        <div className="max-w-4xl w-full">
          <div className="glass-panel p-8 rounded-xl">
            <p className="font-data-label text-data-label text-primary-container uppercase tracking-wider">
              Patient Signup
            </p>
            <h1 className="font-headline-lg text-headline-lg text-primary mt-4">
              Create your patient profile
            </h1>
            <p className="text-on-surface-variant mt-4 leading-relaxed">
              Fill in your personal and medical details so the dashboard can personalize your care plan.
            </p>

            {error && (
              <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
                {error}
              </div>
            )}
            {message && (
              <div className="mt-6 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
                {message}
              </div>
            )}

            <form onSubmit={handleSubmit} className="mt-8 grid gap-4 md:grid-cols-2">
              <label className="text-sm font-semibold text-on-surface-variant">
                Full name
                <input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Date of birth
                <input
                  type="date"
                  name="date_of_birth"
                  value={form.date_of_birth}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Age
                <input
                  type="number"
                  name="age"
                  value={form.age}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  min="0"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Blood group
                <input
                  name="blood_group"
                  value={form.blood_group}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Allergies
                <input
                  name="allergies"
                  value={form.allergies}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  placeholder="None"
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Phone
                <input
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant">
                Email
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  required
                />
              </label>
              <label className="text-sm font-semibold text-on-surface-variant md:col-span-2">
                Address
                <textarea
                  name="address"
                  value={form.address}
                  onChange={handleChange}
                  className="mt-2 w-full rounded-xl border border-outline-variant bg-surface-container-low py-3 px-4 text-sm"
                  rows="3"
                  required
                />
              </label>
              <div className="md:col-span-2 flex justify-end">
                <button
                  type="submit"
                  disabled={loading}
                  className="rounded-xl bg-primary-container text-on-primary-container px-6 py-3 text-sm font-bold disabled:opacity-50"
                >
                  {loading ? "Creating..." : "Create profile"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PatientSignup;
