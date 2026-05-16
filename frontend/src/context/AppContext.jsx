import { createContext, useEffect, useMemo, useState } from "react";

export const AppContext = createContext(null);

const readStoredSelection = (key) => {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const rawValue = window.localStorage.getItem(key);
    return rawValue ? JSON.parse(rawValue) : null;
  } catch {
    return null;
  }
};

export const AppProvider = ({ children }) => {
  const [activeRole, setActiveRole] = useState(() => readStoredSelection("mediflow.activeRole") ?? "admin");
  const [selectedDoctor, setSelectedDoctorState] = useState(() => readStoredSelection("mediflow.selectedDoctor"));
  const [selectedPatient, setSelectedPatientState] = useState(() => readStoredSelection("mediflow.selectedPatient"));
  const [selectedAdmin, setSelectedAdminState] = useState(() => readStoredSelection("mediflow.selectedAdmin"));

  useEffect(() => {
    window.localStorage.setItem("mediflow.activeRole", JSON.stringify(activeRole));
  }, [activeRole]);

  useEffect(() => {
    if (selectedDoctor) {
      window.localStorage.setItem("mediflow.selectedDoctor", JSON.stringify(selectedDoctor));
    } else {
      window.localStorage.removeItem("mediflow.selectedDoctor");
    }
  }, [selectedDoctor]);

  useEffect(() => {
    if (selectedPatient) {
      window.localStorage.setItem("mediflow.selectedPatient", JSON.stringify(selectedPatient));
    } else {
      window.localStorage.removeItem("mediflow.selectedPatient");
    }
  }, [selectedPatient]);

  useEffect(() => {
    if (selectedAdmin) {
      window.localStorage.setItem("mediflow.selectedAdmin", JSON.stringify(selectedAdmin));
    } else {
      window.localStorage.removeItem("mediflow.selectedAdmin");
    }
  }, [selectedAdmin]);

  const setSelectedDoctor = (doctor) => {
    setSelectedDoctorState(doctor);
    setActiveRole("doctor");
  };

  const setSelectedPatient = (patient) => {
    setSelectedPatientState(patient);
    setActiveRole("patient");
  };

  const setSelectedAdmin = (admin) => {
    setSelectedAdminState(admin);
    setActiveRole("admin");
  };

  const value = useMemo(
    () => ({
      activeRole,
      setActiveRole,
      selectedDoctor,
      setSelectedDoctor,
      selectedPatient,
      setSelectedPatient,
      selectedAdmin,
      setSelectedAdmin,
    }),
    [activeRole, selectedDoctor, selectedPatient, selectedAdmin]
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
