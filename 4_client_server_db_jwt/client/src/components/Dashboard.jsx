import React, { Suspense, useState, useEffect } from "react";

import GameCard from "./GameCard";
import GridLoader from "react-spinners/GridLoader";
import { gamesFetch } from "../api";
import StatusDetail from "./StatusDetail";

function Dashboard() {
  const [games, setGames] = useState([]);
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchGames = async () => {
      setMessage("");
      setIsError(false);
      const res = await gamesFetch();
      if (res.ok) {
        const gamesJSON = await res.json();
        setGames(gamesJSON);
      } else {
        const err = await res.json();
        setGames([]);
        setIsError(true);
        setMessage({
          message: "Error fetching games. " + JSON.stringify(err.errors),
        });
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
        {message ? (
          <StatusDetail
            message={message}
            isError={isError}
            onCloseHandler={() => setMessage("")}
          />
        ) : null}
      </Suspense>
    </>
  );
}

export default Dashboard;
