import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Snackbar, Alert } from "@mui/material";

export default function GameForm() {
  const [formData, setFormData] = useState({
    difficulty: "easy",
    range_min: 1,
    range_max: 100,
  });
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");
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
    const message = await res.json();
    setMessage(message);
    setIsError(!res.ok);
    if (res.ok) {
      //onGameRequest(newGame);
      //navigate("/dashboard");
      //navigate("/");
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
    <>
      <form onSubmit={handleSubmit}>
        <h2>New Game</h2>
        <div>
          <label htmlFor="difficulty">Select a level of difficulty:</label>
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
          <label htmlFor="range_min">Minimum value:</label>

          <input
            type="number"
            id="range_min"
            placeholder="Enter minimum"
            value={formData.range_min}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="range_max">Maximum value:</label>

          <input
            type="number"
            id="range_max"
            placeholder="Enter maximum"
            value={formData.range_max}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        open={!!message}
        autoHideDuration={6000}
        onClose={() => setMessage("")}
      >
        <Alert
          severity={isError ? "error" : "success"}
          onClose={() => setMessage("")}
        >
          {message.message}
        </Alert>
      </Snackbar>
    </>
  );
}
