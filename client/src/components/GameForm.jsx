import React, { useState } from "react";

export default function GameForm({
  onGameRequest,
  game = {
    minValue: 1,
    maxValue: 100,
  },
}) {
  const [formData, setFormData] = useState(game);
  const [errors, setErrors] = useState([]);

  async function postGame() {
    const config = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const res = await fetch("/games", config);
    if (res.ok) {
      const newGame = await res.json();
      onGameRequest(newGame);
      setFormData({
        minValue: 1,
        maxValue: 100,
      });
      setErrors([]);
    } else {
      const messages = await res.json();
      setErrors([JSON.stringify(messages.errors)]);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    postGame();
  }

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  }

  return (
    <section>
      <form onSubmit={handleSubmit}>
        <h2>Start New Game</h2>
        <div>
          <label htmlFor="minValue">Minimum value:</label>

          <input
            type="number"
            id="minValue"
            placeholder="Enter minimum"
            value={formData.minValue}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="maxValue">Maximum value:</label>

          <input
            type="number"
            id="maxValue"
            placeholder="Enter maximum"
            value={formData.maxValue}
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
    </section>
  );
}
