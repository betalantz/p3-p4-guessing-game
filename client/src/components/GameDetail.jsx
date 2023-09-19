import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import RoundCard from "./RoundCard";
import GuessForm from "./GuessForm";

function GameDetail() {
  const [{ data: game, error, status }, setGame] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const { id } = useParams();
  const [showGuessForm, setShowGuessForm] = useState(true);

  const fetchGame = useCallback(async () => {
    const response = await fetch(`/games/${id}`);
    if (response.ok) {
      const gameJSON = await response.json();
      setGame({ data: gameJSON, error: null, status: "resolved" });
    } else {
      const gameErr = await response.json();
      setGame({ data: null, error: gameErr, status: "rejected" });
    }
  }, [id]);

  useEffect(() => {
    fetchGame().catch(console.error);
  }, [id, fetchGame]);

  function handleUpdateGame(updatedGame) {
    fetchGame();
    setShowGuessForm(!updatedGame.is_over);
  }

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2>Error: {error.error}</h2>;

  return (
    <div>
      <h2>Game {game.id}</h2>

      {showGuessForm ? (
        <GuessForm game={game} onGuessRequest={handleUpdateGame} />
      ) : (
        <p>
          Congratulations! You guessed the secret number {game.secret_number}!
        </p>
      )}
      <hr />
      <h2>Rounds:</h2>
      <div className="roundList">
        <ul>
          {game.rounds.map((round, index) =>
            round.status ? (
              <RoundCard
                key={index}
                round={round}
                game_min={game.min_value}
                game_max={game.max_value}
              />
            ) : null
          )}
        </ul>
      </div>
    </div>
  );
}

export default GameDetail;
