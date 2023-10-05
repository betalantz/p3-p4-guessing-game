import { 
    createContext,
    useContext,
    useMemo,
    useState,
} from "react";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [token, setToken_] = useState(null);

    const setToken = (newToken) => setToken_(newToken);

    const contextValue = useMemo(
        () => ({ token, setToken }),
        [token, setToken]
    );
    
    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);

export default AuthProvider;