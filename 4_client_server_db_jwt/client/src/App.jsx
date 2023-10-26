import React, { Suspense, useEffect, useState } from "react";
import { useAuth } from "./providers/authProvider";
import { refreshFetch } from "./api";
import Routes from "./routes/Routes";
import TokenVerify from "./routes/TokenVerify";
import GridLoader from "react-spinners/GridLoader";

function App() {
  const { token, setToken } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    const fetchRefresh = async () => {
      const res = await refreshFetch();
      if (res.ok) {
        const tokenJSON = await res.json();
        setToken(tokenJSON);
      } else {
        setToken(null);
      }
      setIsLoading(false);
    };

    fetchRefresh();
  }, []);

  if (isLoading) return <GridLoader />;

  return (
    <div>
      <main>
        <Routes />
      </main>
    </div>
  );
}

export default App;
