import React, { Suspense, useState, useEffect } from "react";
import GameCard from "./GameCard";
import GameForm from "./GameForm";
import GridLoader from "react-spinners/GridLoader";

function Dashboard({games, handleDeleteGame}) {
  

  let gameCards = games.map((game) => (
    <GameCard key={game.id} game={game} onDelete={handleDeleteGame} />
  ));

  return (
    <>
      <Suspense fallback={<GridLoader />}>
        <h1>Your Games</h1>
        <div className="gameList">{gameCards}</div>
      </Suspense>
    </>
  );
}

export default Dashboard;
