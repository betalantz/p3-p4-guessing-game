import React from "react";
import { Link } from "react-router-dom";

function GameCard({
  game: { id, is_over, min_value, max_value, secret_number, rounds },
  onDelete,
}) {
  return (
    <div className="gameCard">
      <h3>Game {id}</h3>
      <p>
        Guessing range is {min_value} .. {max_value}
      </p>
      {is_over ? (
        <p>
          It took {rounds.length} guesses to guess the secret number{" "}
          {secret_number}.
        </p>
      ) : null}

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
