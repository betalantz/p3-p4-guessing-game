import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [token, setToken_] = useState(null);

  const contextValue = useMemo(() => {
    const setToken = (newToken) => setToken_(newToken);
    return { token, setToken };
  }, [token]);

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export default AuthProvider;
