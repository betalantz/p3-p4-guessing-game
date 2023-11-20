import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import RoundCard from "./RoundCard";

function GameDetail() {
  const [rounds, setRounds] = useState([]);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState("pending");
  const { id } = useParams();

  const fetchGameRounds = useCallback(async () => {
    const response = await fetch(`/games/${id}/rounds`);
    if (response.ok) {
      const roundsJSON = await response.json();
      setRounds(roundsJSON);
      setError(null);
      setStatus("resolved");
    } else {
      const err = await response.json();
      setRounds([]);
      setError(err);
      setStatus("rejected");
    }
  }, [id]);

  useEffect(() => {
    fetchGameRounds().catch(console.error);
  }, [id, fetchGameRounds]);

  function handleUpdateGame() {
    fetchGameRounds();
  }

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2 style={{ color: "red" }}>Error: {error.status}</h2>;

  return (
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
  );
}

export default GameDetail;
