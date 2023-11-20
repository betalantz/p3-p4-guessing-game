import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function GameForm({ onGameRequest }) {
  const initFormState = {
    difficulty: "easy",
    range_min: 1,
    range_max: 100,
  };
  const [formData, setFormData] = useState(initFormState);
  const [errors, setErrors] = useState([]);
  const navigate = useNavigate();

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
      setFormData(initFormState);
      setErrors([]);
      navigate("/");
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
          <label htmlFor="difficulty">Select a level of difficulty:</label>{" "}
          <select
            id="difficulty"
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
          >
            <option key={"difficulty_easy"}>easy</option>
            <option key={"difficulty_hard"}>hard</option>
          </select>
        </div>

        <div>
          <label htmlFor="range_min">Minimum value:</label>{" "}
          <input
            type="number"
            id="range_min"
            placeholder="Enter minimum"
            value={formData.range_min}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="range_max">Maximum value:</label>{" "}
          <input
            type="number"
            id="range_max"
            placeholder="Enter maximum"
            value={formData.range_max}
            onChange={handleChange}
          />
        </div>
        {errors.length > 0 &&
          errors.map((err) => (
            <p key={err} style={{ color: "red" }}>
              {err}
            </p>
          ))}
        <button type="submit">Submit</button>
      </form>
    </section>
  );
}
