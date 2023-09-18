import React from "react";
import { Link } from "react-router-dom";

function GameCard({
  game: { id, is_over, secret_number, current_round, rounds },
  onDelete,
}) {
  return (
    <div className="gameCard">
      <h3>Game {id}</h3>
      <p>
        Guessing range is {rounds[0].min_value} .. {rounds[0].max_value}
      </p>
      {current_round.status === "Status.CORRECT" ? (
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
