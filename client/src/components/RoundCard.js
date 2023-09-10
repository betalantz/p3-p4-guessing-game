import React from "react";
import Stack from "@mui/material/Stack";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import Status from "./Status";

function RoundCard({ round, isHighlightRound }) {
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
  return (
    <li>
      <Stack spacing={1} direction="row" sx={{ mt: 2 }} alignItems="center">
        <Box sx={{ width: 300, padding: 2 }}>
          <Slider
            value={round.guess}
            valueLabelDisplay="on"
            min={round.minValue}
            max={round.maxValue}
            marks={marks}
            disabled
          />
        </Box>
        <div className={isHighlightRound ? "highlightRound" : null}>
          <Status status={round.status} />
        </div>
      </Stack>
    </li>
  );
}

export default RoundCard;
