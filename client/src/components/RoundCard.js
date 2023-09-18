import React from "react";
import Stack from "@mui/material/Stack";
import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import Status from "./Status";

function RoundCard({ round, game_min, game_max }) {
  const marks = [
    {
      value: round.min_value,
      label: round.min_value,
    },
    {
      value: round.max_value,
      label: round.max_value,
    },
  ];
  return (
    <li>
      <Stack spacing={1} direction="row" sx={{ mt: 2 }} alignItems="center">
        <Box sx={{ width: 600, padding: 1 }}>
          <Slider
            value={round.guess}
            valueLabelDisplay="on"
            min={game_min}
            max={game_max}
            marks={marks}
            disabled
          />
        </Box>
        <div>
          <Status status={round.status} />
        </div>
      </Stack>
    </li>
  );
}

export default RoundCard;
