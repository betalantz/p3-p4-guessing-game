import React, { Suspense, useEffect, useState } from "react";
import { useAuth } from "./providers/authProvider";
import { authenticateFetch } from "./api";
import Routes from "./routes/Routes";
import GridLoader from "react-spinners/GridLoader";

function App() {
  const { token, setToken } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    const fetchAuth = async () => {
      const res = await authenticateFetch();
      if (res.ok) {
        const tokenJSON = await res.json();
        setToken(tokenJSON);
      } else {
        setToken(null);
      }
      setIsLoading(false);
    };

    fetchAuth();
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
