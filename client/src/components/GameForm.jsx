import React, { useState } from "react";

export default function GameForm({ onGameRequest }) {
  const [formData, setFormData] = useState({
    level: "easy",
    min_value: 1,
    max_value: 100,
  });
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
        level: "easy",
        min_value: 1,
        max_value: 100,
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
        <h2>New Game</h2>
        <div>
          <label htmlFor="level">Select a difficulty level:</label>
          <select
            id="level"
            name="level"
            value={formData.level}
            onChange={handleChange}
          >
            <option key={"level_easy"}>easy</option>
            <option key={"level_hard"}>hard</option>
          </select>
        </div>

        <div>
          <label htmlFor="min_value">Minimum value:</label>

          <input
            type="number"
            id="min_value"
            placeholder="Enter minimum"
            value={formData.min_value}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="max_value">Maximum value:</label>

          <input
            type="number"
            id="max_value"
            placeholder="Enter maximum"
            value={formData.max_value}
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
