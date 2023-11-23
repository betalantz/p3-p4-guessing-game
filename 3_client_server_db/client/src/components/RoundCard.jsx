import React, { useState, useEffect } from "react";
import Stack from "@mui/material/Stack";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";

function RoundCard({ round, onGuessRequest }) {
  const [isCurrentRound, setIsCurrentRound] = useState(false);
  const [guess, setGuess] = useState(0);
  const [errors, setErrors] = useState([]);
  const [marks, setMarks] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    setIsCurrentRound(!round.status);
  }, [round]);

  useEffect(() => {
    isCurrentRound ? setGuess(round.range_min) : setGuess(round.guess);
    setMarks([
      {
        value: round.range_min,
        label: round.range_min,
      },
      {
        value: round.range_max,
        label: round.range_max,
      },
    ]);
    switch (round.status) {
      case "correct":
        setStatusMessage(`${round.guess} is correct!`);
        break;
      case "low":
        setStatusMessage(`${round.guess} is too low.`);
        break;
      case "high":
        setStatusMessage(`${round.guess} is too high.`);
        break;
      case "invalid":
        setStatusMessage(
          `${round.guess} is outside the valid range of numbers.`
        );
        break;
      default:
        setStatusMessage(
          `Guess a number from ${round.range_min} to ${round.range_max}.`
        );
    }
  }, [round, isCurrentRound]);

  async function updateGame() {
    const updateData = {
      guess: parseInt(guess),
      round_id: round.id,
    };
    const config = {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    };
    const res = await fetch(`/games/${round.game.id}`, config);
    if (res.ok) {
      const updGame = await res.json();
      onGuessRequest(updGame);
      setGuess(round.range_min);
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
    <li>
      <form onSubmit={handleSubmit}>
        <Stack spacing={1} direction="row" sx={{ mt: 2 }} alignItems="center">
          <Box sx={{ width: 400 }}>
            <Slider
              value={guess}
              valueLabelDisplay="on"
              min={round.range_min}
              max={round.range_max}
              marks={marks}
              track={false}
              disabled={!isCurrentRound}
              onChange={handleChange}
            />
          </Box>
          <Box sx={{ width: 200, padding: 2 }}>
            <p>{statusMessage}</p>
            {isCurrentRound ? <button type="submit">Submit</button> : null}
          </Box>
        </Stack>
      </form>
      {errors.length > 0 && errors.map((err) => (
        <p key={err} style={{ color: "red" }}>
          {err}
        </p>
      ))}
    </li>
  );
}

export default RoundCard;
