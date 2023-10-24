import React, { useState } from "react";
//import { useNavigate } from "react-router-dom";
import { postGamesFetch, newRoundByGameIdFetch } from "../api";
import StatusDetail from "./StatusDetail";

export default function GameForm() {
  function initFormData() {
    return {
      difficulty: "easy",
      range_min: 1,
      range_max: 100,
    };
  }
  const [formData, setFormData] = useState(initFormData());
  const [isError, setIsError] = useState(false);
  const [message, setMessage] = useState("");
  //const navigate = useNavigate();

  async function postGame() {
    setMessage("");
    setIsError(false);
    const res = await postGamesFetch(formData);
    if (res.ok) {
      const gameJSON = await res.json();
      await newRoundByGameIdFetch(gameJSON.id);
      setMessage({ message: "New game added." });
      setFormData(initFormData());
      //navigate("/dashboard");
    } else {
      const err = await res.json();
      setIsError(true);
      setMessage({
        message: "Error adding game. " + JSON.stringify(err.errors),
      });
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
      {message ? (
        <StatusDetail
          message={message}
          isError={isError}
          onCloseHandler={() => setMessage("")}
        />
      ) : null}
    </>
  );
}
