import React, { useState, useEffect } from "react";

export default function GameRoundForm({ round, onPlayRound }) {
  const [guess, setGuess] = useState(round.minValue);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    setGuess(round.minValue);
  }, [round.minValue]);

  async function postRound() {
    const postData = {
      id: round.id,
      minValue: round.minValue,
      maxValue: round.maxValue,
      guess: parseInt(guess),
    };
    const config = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    };
    const res = await fetch("/round", config);
    if (res.ok) {
      const playedRound = await res.json();
      onPlayRound(playedRound);
      setGuess(round.minValue);
      setErrors([]);
    } else {
      const messages = await res.json();
      setErrors([JSON.stringify(messages.errors)]);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    postRound();
  }

  function handleChange(e) {
    setGuess(e.target.value);
  }

  return (
    <section>
      <form onSubmit={handleSubmit}>
        <p>
          Guess a number between {round.minValue} and {round.maxValue}.
          <input
            type="number"
            id="guess"
            defaultValue={guess}
            min={round.minValue}
            max={round.maxValue}
            onChange={handleChange}
            required
          />
          <br></br>
          <button type="submit">Submit</button>
        </p>
        {errors.map((err) => (
          <p key={err} style={{ color: "red" }}>
            {err}
          </p>
        ))}
      </form>
    </section>
  );
}
