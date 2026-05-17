import { useEffect, useState } from "react";

import Navbar from "../../components/Navbar.jsx";
import { createAdminDoctor, createAdminPatient, getAdminDepartments } from "../../api/index.js";

const emptyPatient = {
  name: "",
  date_of_birth: "",
  age: "",
  blood_group: "",
  allergies: "",
  phone: "",
  email: "",
  address: "",
};

const emptyDoctor = {
  name: "",
  department_id: "",
  specialization: "",
  is_available: true,
};

const CreateAccount = () => {
  const [activeTab, setActiveTab] = useState("patient");
  const [departments, setDepartments] = useState([]);
  const [patientForm, setPatientForm] = useState(emptyPatient);
  const [doctorForm, setDoctorForm] = useState(emptyDoctor);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getAdminDepartments()
      .then((response) => {
        setDepartments(response.data.departments ?? []);
      })
      .catch((err) => {
        console.error("Failed to load departments:", err);
      });
  }, []);

  const handlePatientChange = (event) => {
    const { name, value } = event.target;
    setPatientForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleDoctorChange = (event) => {
    const { name, value, type, checked } = event.target;
    setDoctorForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const submitPatient = async (event) => {
    event.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      const payload = {
        ...patientForm,
        age: patientForm.age ? Number(patientForm.age) : null,
      };
      const response = await createAdminPatient(payload);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setMessage(response.data.message ?? "Patient account created.");
        setPatientForm(emptyPatient);
      }
    } catch (err) {
      console.error("Create patient failed:", err);
      setError(err.response?.data?.error || "Failed to create patient.");
    } finally {
      setLoading(false);
    }
  };

  const submitDoctor = async (event) => {
    event.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      const payload = {
        ...doctorForm,
        department_id: Number(doctorForm.department_id),
      };
      const response = await createAdminDoctor(payload);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setMessage(response.data.message ?? "Doctor account created.");
        setDoctorForm(emptyDoctor);
      }
    } catch (err) {
      console.error("Create doctor failed:", err);
      setError(err.response?.data?.error || "Failed to create doctor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <Navbar title="Create Account" subtitle="Admin-only account creation" />

      {error && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
          {error}
        </div>
      )}
      {message && (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
          {message}
        </div>
      )}

      <div className="rounded-2xl bg-white border border-slate-200 p-6">
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => setActiveTab("patient")}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
              activeTab === "patient"
                ? "bg-blue-600 text-white"
                : "border border-slate-200 text-slate-600"
            }`}
          >
            Create Patient
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("doctor")}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
              activeTab === "doctor"
                ? "bg-blue-600 text-white"
                : "border border-slate-200 text-slate-600"
            }`}
          >
            Create Doctor
          </button>
        </div>

        {activeTab === "patient" ? (
          <form onSubmit={submitPatient} className="mt-6 grid gap-4 md:grid-cols-2">
            <label className="text-sm font-semibold text-slate-600">
              Full name
              <input
                name="name"
                value={patientForm.name}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Date of birth
              <input
                type="date"
                name="date_of_birth"
                value={patientForm.date_of_birth}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Age
              <input
                type="number"
                name="age"
                value={patientForm.age}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                min="0"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Blood group
              <input
                name="blood_group"
                value={patientForm.blood_group}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Allergies
              <input
                name="allergies"
                value={patientForm.allergies}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                placeholder="None"
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Phone
              <input
                name="phone"
                value={patientForm.phone}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Email
              <input
                type="email"
                name="email"
                value={patientForm.email}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600 md:col-span-2">
              Address
              <textarea
                name="address"
                value={patientForm.address}
                onChange={handlePatientChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                rows="3"
                required
              />
            </label>
            <div className="md:col-span-2 flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="rounded-full bg-blue-600 px-6 py-2 text-sm font-semibold text-white disabled:opacity-50"
              >
                {loading ? "Saving..." : "Create patient"}
              </button>
            </div>
          </form>
        ) : (
          <form onSubmit={submitDoctor} className="mt-6 grid gap-4 md:grid-cols-2">
            <label className="text-sm font-semibold text-slate-600">
              Full name
              <input
                name="name"
                value={doctorForm.name}
                onChange={handleDoctorChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              />
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Department
              <select
                name="department_id"
                value={doctorForm.department_id}
                onChange={handleDoctorChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
                required
              >
                <option value="">Select department</option>
                {departments.map((dept) => (
                  <option key={dept.id} value={dept.id}>
                    {dept.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-sm font-semibold text-slate-600">
              Specialization
              <input
                name="specialization"
                value={doctorForm.specialization}
                onChange={handleDoctorChange}
                className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
              />
            </label>
            <label className="text-sm font-semibold text-slate-600 flex items-center gap-2">
              <input
                type="checkbox"
                name="is_available"
                checked={doctorForm.is_available}
                onChange={handleDoctorChange}
              />
              Available for appointments
            </label>
            <div className="md:col-span-2 flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="rounded-full bg-blue-600 px-6 py-2 text-sm font-semibold text-white disabled:opacity-50"
              >
                {loading ? "Saving..." : "Create doctor"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default CreateAccount;
