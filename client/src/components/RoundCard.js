import React from "react";
import Stack from "@mui/material/Stack";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import Status from "./Status";

function RoundCard({
  round: { min_value, max_value, guess, status },
  game_min,
  game_max,
}) {
  const marks = [
    {
      value: min_value,
      label: min_value,
    },
    {
      value: max_value,
      label: max_value,
    },
  ];
  return (
    <li>
      <Stack spacing={1} direction="row" sx={{ mt: 2 }} alignItems="center">
        <Box sx={{ width: 600, padding: 1 }}>
          <Slider
            value={guess}
            valueLabelDisplay="on"
            min={game_min}
            max={game_max}
            marks={marks}
            track={false}
          />
        </Box>
        <div>
          <Status status={status} />
        </div>
      </Stack>
    </li>
  );
}

export default RoundCard;
