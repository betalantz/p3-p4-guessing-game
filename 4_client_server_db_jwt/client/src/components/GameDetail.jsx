import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import RoundCard from "./RoundCard";
import { gamesByIdFetch } from "../api";

function GameDetail() {
  const [game, setGame] = useState({ secret_number: 0 });
  const [error, setError] = useState(null);
  const [status, setStatus] = useState("pending");
  const { id } = useParams();

  const fetchGame = useCallback(async () => {
    const res = await gamesByIdFetch(id);

    if (res.ok) {
      const gameJSON = await res.json();
      setGame(gameJSON);
      setError(null);
      setStatus("resolved");
    } else {
      const err = await res.json();
      setGame(null);
      setError(err);
      setStatus("rejected");
    }
  }, [id]);

  useEffect(() => {
    fetchGame().catch(console.error);
  }, [id, fetchGame]);

  function handleUpdateGame() {
    fetchGame();
  }

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2>Error: {error}</h2>;

  return (
    <div>
      <h2>Game {game.id}</h2>
      <div className="roundList">
        <ul>
          {game.rounds.reverse().map((round, index) => (
            <RoundCard
              key={index}
              round={round}
              game={game}
              onGuessRequest={handleUpdateGame}
            />
          ))}
        </ul>
      </div>
    </div>
  );
}

export default GameDetail;
