import { createContext, useContext, useState } from "react";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [pile, setPile] = useState(localStorage.getItem("pileId") || "");
  const [documents, setDocuments] = useState([]);
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pilename, setPileName] = useState(
    localStorage.getItem("pilename") || "",
  );

  const clearError = () => {
    setError("");
  };

  return (
    <AppContext.Provider
      value={{
        pile,
        setPile,
        documents,
        setDocuments,
        run,
        setRun,
        loading,
        setLoading,
        error,
        setError,
        clearError,
        pilename,
        setPileName,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);

  if (!context) {
    throw new Error("useApp must be used inside AppProvider");
  }

  return context;
}
