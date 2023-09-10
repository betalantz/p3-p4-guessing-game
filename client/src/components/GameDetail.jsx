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
  const [showGuess, setShowGuess] = useState(true);

  const fetchGame = useCallback(async () => {
    const res = await fetch(`/games/${id}`);
    if (res.ok) {
      const gameJSON = await res.json();
      setGame({ data: gameJSON, error: null, status: "resolved" });
    } else {
      const gameErr = await res.json();
      setGame({ data: null, error: gameErr, status: "rejected" });
    }
  }, [id]);

  useEffect(() => {
    fetchGame().catch(console.error);
  }, [id, fetchGame]);

  function handleUpdateGame(updatedGame) {
    setGame({ data: updatedGame, error: null, status: "resolved" });
    setShowGuess(!updatedGame.isOver);
  }

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2>Error: {error.error}</h2>;

  return (
    <div>
      <h2>Game #{game.id}</h2>

      {showGuess ? (
        <GuessForm game={game} onGuessRequest={handleUpdateGame} />
      ) : (
        <p>
          Congratulations! You guessed the secret number {game.secretNumber}!
        </p>
      )}
      <hr />
      <h2>Rounds:</h2>
      <div className="roundList">
        <ul>
          {game?.rounds.toReversed().map((r, index) => (
            <RoundCard key={index} round={r} isHighlightRound={index === 0} />
          ))}
        </ul>
      </div>
    </div>
  );
}

export default GameDetail;
