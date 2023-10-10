import React, { Suspense, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import GameDetail from "./components/GameDetail";
import { useAuth } from "./providers/authProvider";
import { authenticateFetch } from "./api";
import Routes from "./routes/Routes";
import GridLoader from "react-spinners/GridLoader";

function App() {
  const { token, setToken } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [games, setGames] = useState([]);

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

  useEffect(() => {
    const fetchGames = async () => {
      const response = await fetch("/games");
      const gameArr = await response.json();
      setGames(gameArr);
    };
    fetchGames().catch(console.error);
  }, []);

  function handleAddGame(newGame) {
    setGames((games) => [...games, newGame]);
  }

  function handleDeleteGame(id) {
    fetch(`/games/${id}`, { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setGames((games) => games.filter((games) => games.id !== id));
      }
    });
  }

  if (isLoading) return <GridLoader />;

  return (
    <div>
      <main>
        <Routes
          games={games}
          handleAddGame={handleAddGame}
          handleDeleteGame={handleDeleteGame}
        />
      </main>
    </div>
  );
}

export default App;
