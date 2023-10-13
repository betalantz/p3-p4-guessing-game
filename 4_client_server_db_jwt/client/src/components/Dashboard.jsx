import React, { Suspense, useState, useEffect, useCallback } from "react";

import GameCard from "./GameCard";
import GridLoader from "react-spinners/GridLoader";

function Dashboard() {
  const [games, setGames] = useState([]);
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");

  const fetchGames = useCallback(async () => {
    const response = await fetch("/games");
    if (response.ok) {
      const gamesJSON = await response.json();
      setGames(gamesJSON);
      setIsError(false);
      setMessage("");
    } else {
      const err = await response.json();
      setGames([]);
      setIsError(true);
      setMessage(err);
    }
  }, []);

  useEffect(() => {
    fetchGames().catch(console.error);
  }, [fetchGames]);

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

  let gameCards = games.map((game) => (
    <GameCard key={game.id} game={game} onDelete={handleDeleteGame} />
  ));

  return (
    <>
      <Suspense fallback={<GridLoader />}>
        <h1>Your Games</h1>
        <div className="gameList">{gameCards}</div>
      </Suspense>
      {isError && <p style={{ color: "red" }}>{message}</p>}
    </>
  );
}

export default Dashboard;
