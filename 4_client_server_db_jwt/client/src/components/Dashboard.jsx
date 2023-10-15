import React, { Suspense, useState, useEffect } from "react";

import GameCard from "./GameCard";
import GridLoader from "react-spinners/GridLoader";

function Dashboard() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchGames = async () => {
      const res = await fetch("/games");
      if (res.ok) {
        const gamesJSON = await res.json();
        setGames(gamesJSON);
      } else {
        setGames([]);
      }
    };

    fetchGames();
  }, []);

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
    </>
  );
}

export default Dashboard;
