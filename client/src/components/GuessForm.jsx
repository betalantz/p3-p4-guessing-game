import React, { useState, useEffect } from "react";

export default function GuessForm({
  game,
  round = {
    guess: 0,
  },
  onGuessRequest,
}) {
  const [guess, setGuess] = useState(round.minValue);
  const [errors, setErrors] = useState([]);
  const [isShowHint, setIsShowHint] = useState(false);

  useEffect(() => {
    setGuess(game.minValue);
  }, [game.minValue]);

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
      setGuess(0);
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
          Guess a number from {game.minValue} to {game.maxValue}.
        </h2>
        <div>
          <label htmlFor="guess">Enter Guess:</label>
          <input
            type="number"
            id="guess"
            placeholder="Enter guess"
            defaultValue={guess}
            min={game.minValue}
            max={game.maxValue}
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
          <span>What is {game.secretNumber - 2 ** 4} + (2**4)?</span>
        ) : null}
      </div>
    </section>
  );
}
