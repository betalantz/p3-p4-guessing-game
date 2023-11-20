import React, { Suspense, useState, useEffect } from "react";
import GameCard from "./GameCard";
import GameForm from "./GameForm";
import GridLoader from "react-spinners/GridLoader";
import { IconButton } from "@mui/material";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { Link as RouterLink } from "react-router-dom";

function Dashboard({ games, handleDeleteGame }) {
  let gameCards = games.map((game) => (
    <GameCard key={game.id} game={game} onDelete={handleDeleteGame} />
  ));

  return (
    <>
      <Suspense fallback={<GridLoader />}>
        <IconButton component={RouterLink} to="/games/new">
          <AddCircleIcon fontSize="large" color="primary"/>
        </IconButton>
        <h1>Your Games</h1>
        <div className="gameList">{gameCards}</div>
      </Suspense>
      <hr />
    </>
  );
}

export default Dashboard;
