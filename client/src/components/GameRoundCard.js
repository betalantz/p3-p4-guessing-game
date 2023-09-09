import React from "react";
import Stack from "@mui/material/Stack";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import Status from "./Status";

function GameRoundCard({ round, currentRound }) {
  const marks = [
    {
      value: round.minValue,
      label: round.minValue,
    },
    {
      value: round.maxValue,
      label: round.maxValue,
    },
  ];
  const liClass = currentRound ? "currentRound" : null;
  return (
    <li className={liClass}>
      <Stack spacing={1} direction="row" sx={{ mt: 4 }} alignItems="center">
        <Box sx={{ width: 300, padding: 2 }}>
          <Slider
            value={round.guess}
            valueLabelDisplay="on"
            min={1}
            max={100}
            marks={marks}
            disabled
          />
        </Box>
        <Status status={round.status} />
      </Stack>
    </li>
  );
}

export default GameRoundCard;
