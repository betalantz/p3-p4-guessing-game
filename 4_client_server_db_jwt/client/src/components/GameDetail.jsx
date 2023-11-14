import React, { useState, useEffect, useCallback, Suspense } from "react";
import { useParams } from "react-router-dom";
import GridLoader from "react-spinners/GridLoader";
import RoundCard from "./RoundCard";
import { roundsByGameIdFetch } from "../api";
import { useAuth } from "../providers/authProvider";

function GameDetail() {
  const [rounds, setRounds] = useState([]);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState("pending");
  const { id } = useParams();
  const { isTokenExpired } = useAuth();

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
      fetchRounds().catch(console.error);
    }
  }, [id, fetchRounds, isTokenExpired]);

  function handleUpdateGame() {
    fetchRounds().catch(console.error);
  }

  if (status === "pending") return <GridLoader />;
  if (status === "rejected") return <h2 color="red">Error: {error.message}</h2>;

  return (
    <Suspense fallback={<GridLoader />}>
      <div>
        <h2>Game {id}</h2>
        <div className="roundList">
          <ul>
            {rounds
              .sort((a, b) => b.number - a.number)
              .map((round, index) => (
                <RoundCard
                  key={index}
                  round={round}
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
