import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [token, setToken_] = useState(null);
  const isTokenExpired = () => {
    if (!token) {
      return true;
    }
    const payload = token.access_token.split('.')[1];
    const { exp } = JSON.parse(atob(payload));
    if (!exp) {
      return true;
    }
  
    return Date.now() >= exp * 1000;
  }

  const contextValue = useMemo(() => {
    const setToken = (newToken) => setToken_(newToken);
    return { token, setToken, isTokenExpired };
  }, [token]);

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export default AuthProvider;
