import React, { Suspense, useState, useEffect } from "react";
import GameCard from "./GameCard";
import GameForm from "./GameForm";
import GridLoader from "react-spinners/GridLoader";

function Dashboard() {
  const [games, setGames] = useState([]);

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

  let gameCards = games.map((game) => (
    <GameCard key={game.id} game={game} onDelete={handleDeleteGame} />
  ));

  return (
    <>
      <Suspense fallback={<GridLoader />}>
        <h1>Your Games</h1>
        <div className="gameList">{gameCards}</div>
      </Suspense>
      <hr />
      <GameForm onGameRequest={handleAddGame} />
    </>
  );
}

export default Dashboard;
