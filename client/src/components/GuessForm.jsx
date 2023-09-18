import React, { useState, useEffect } from "react";

export default function GuessForm({
  game,
  round = {
    guess: 0,
  },
  onGuessRequest,
}) {
  const [guess, setGuess] = useState();
  const [errors, setErrors] = useState([]);
  const [isShowHint, setIsShowHint] = useState(false);
  const [rand, setRand] = useState();

  useEffect(() => {
    setGuess(game.current_round.min_value);
    setRand(Math.floor(Math.random() * 3) + 3); //3..5
  }, [game]);

  async function updateGame() {
    const updateData = {
      guess: parseInt(guess),
    };
    const config = {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    };
    const res = await fetch(`/games/${game.id}`, config);
    if (res.ok) {
      const updGame = await res.json();
      onGuessRequest(updGame);
      setGuess(updGame.current_round.min_value);
      setErrors([]);
    } else {
      const messages = await res.json();
      setErrors([JSON.stringify(messages.errors)]);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    updateGame();
  }

  function handleChange(e) {
    setGuess(e.target.value);
  }

  return (
    <section>
      <form onSubmit={handleSubmit}>
        <h2>
          Guess a number from {game.current_round.min_value} to{" "}
          {game.current_round.max_value}.
        </h2>
        <div>
          <label htmlFor="guess">Enter Guess:</label>
          <input
            type="number"
            id="guess"
            placeholder="Enter guess"
            defaultValue={guess}
            min={game.current_round.min_value}
            max={game.current_round.max_value}
            onChange={handleChange}
          />
        </div>
        {errors.map((err) => (
          <p key={err} style={{ color: "red" }}>
            {err}
          </p>
        ))}
        <button type="submit">Submit</button>
      </form>
      <div className="toggle-switch">
        <label>Hint</label>
        <input
          type="checkbox"
          id="toggle-show-hint"
          checked={isShowHint}
          onChange={(e) => setIsShowHint(e.target.checked)}
        />

        <label htmlFor="toggle-show-hint"></label>
        {isShowHint ? (
          <span>
            What is {game.secret_number - 2 ** rand} + (2**{rand})?
          </span>
        ) : null}
      </div>
    </section>
  );
}
