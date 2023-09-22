import React from "react";
import { Link } from "react-router-dom";

function GameCard({
  game: { id, level, secret_number, is_over, min_value, max_value, rounds },
  onDelete,
}) {
  return (
    <div className="gameCard">
      <h3>Game {id}</h3>
      <p>
        Difficulty level is {level}. Guessing range is {min_value} ..{" "}
        {max_value}.
      </p>
      {is_over && (
        <p>
          You guessed the secret number {secret_number} in {rounds.length}{" "}
          guesses.
        </p>
      )}

      <Link to={`/games/${id}`}>
        {" "}
        <button type="button" disabled={is_over}>
          Play Game
        </button>
      </Link>
      <Link to="/dashboard"></Link>
      <span>
        {" "}
        <button onClick={() => onDelete(id)}>Delete Game</button>
      </span>
    </div>
  );
}

export default GameCard;
