import React from "react";
import { Link } from "react-router-dom";

function GameCard({ game: { id, minValue, maxValue, isOver }, onDelete }) {
  return (
    <div className="gameCard">
      <h3>Game #{id}</h3>
      <p>
        Guessing range is {minValue}..{maxValue}.
      </p>
      <Link to={`/games/${id}`}>
        {" "}
        <button type="button" disabled={isOver}>
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
