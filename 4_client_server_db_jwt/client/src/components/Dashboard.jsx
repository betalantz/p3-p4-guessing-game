import React, { Suspense, useState, useEffect } from "react";

import GameCard from "./GameCard";
import GridLoader from "react-spinners/GridLoader";
import { gamesFetch, deleteGamesByIdFetch } from "../api";
import { useGames } from "../providers/gamesProvider";
import { useAuth } from "../providers/authProvider";
import StatusDetail from "./StatusDetail";

function Dashboard() {
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");
  const { games, setGames } = useGames();
  const { isTokenExpired } = useAuth();

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
    if (!isTokenExpired()) {
      fetchGames();
    }
  }, [isTokenExpired, setGames]);

  async function deleteGame(id) {
    const res = await deleteGamesByIdFetch(id);
    if (res.ok) {
      setGames((games) => games.filter((games) => games.id !== id));
    } else {
      const err = await res.json();
      setGames([]);
      setIsError(true);
      setMessage({
        message: "Error deleting game. " + JSON.stringify(err.errors),
      });
    }
  }

  let gameCards = games
    .sort((a, b) => a.number - b.number) // sort by number
    .map((game) => (
      <GameCard key={game.id} game={game} onDelete={deleteGame} />
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
