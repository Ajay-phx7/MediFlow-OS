import { createContext, useMemo, useState } from "react";

export const AppContext = createContext(null);

export const AppProvider = ({ children }) => {
  const [activeRole, setActiveRole] = useState("admin");

  const value = useMemo(
    () => ({
      activeRole,
      setActiveRole,
    }),
    [activeRole]
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
