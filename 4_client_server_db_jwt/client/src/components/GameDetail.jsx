import React, { useState, useEffect, useCallback, Suspense } from "react";
import { useParams } from "react-router-dom";
import GridLoader from "react-spinners/GridLoader";
import RoundCard from "./RoundCard";
import {
  gamesByIdFetch,
  roundsByGameIdFetch,
  newRoundByGameIdFetch,
} from "../api";
import { useAuth } from "../providers/authProvider";

function GameDetail() {
  const [game, setGame] = useState({ secret_number: 0 });
  const [rounds, setRounds] = useState([]);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState("pending");
  const { id } = useParams();
  const { isTokenExpired } = useAuth();

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

  const fetchRounds = useCallback(async () => {
    const res = await roundsByGameIdFetch(id);

    if (res.ok) {
      const roundsJSON = await res.json();
      setRounds(roundsJSON);
      setError(null);
      setStatus("resolved");
    } else {
      const err = await res.json();
      setRounds([]);
      setError(err);
      setStatus("rejected");
    }
  }, [id]);

  useEffect(() => {
    if (!isTokenExpired()) {
      fetchGame().catch(console.error);
      fetchRounds().catch(console.error);
    }
  }, [id, fetchGame, fetchRounds, isTokenExpired]);

  function handleUpdateGame() {
    fetchGame().catch(console.error);
    fetchRounds().catch(console.error);
  }

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2>Error: {error}</h2>;

  return (
    <Suspense fallback={<GridLoader />}>
      <div>
        <h2>Game {game.id}</h2>
        <div className="roundList">
          <ul>
            {rounds.reverse().map((round, index) => (
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
    </Suspense>
  );
}

export default GameDetail;
