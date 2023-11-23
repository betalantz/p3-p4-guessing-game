import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import GameDetail from "./components/GameDetail";
import GameForm from "./components/GameForm";

function App() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchGames = async () => {
      const response = await fetch("/games");
      const gameArr = await response.json();
      setGames(gameArr);
    };
    fetchGames().catch(console.error);
  }, []);

  function handleAddGame(newGame) {
    setGames((games) => [...games, newGame]); // optimistic rendering
  }

  function handleUpdateGame(updatedGame) {
    setGames((games) =>
      games.map((game) => (game.id === updatedGame.id ? updatedGame : game))
    );
  }

  function handleDeleteGame(id) {
    fetch(`/games/${id}`, { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setGames((games) => games.filter((games) => games.id !== id)); //optimistic rendering
      }
    });
  }
  return (
    <div>
      <Header />
      <main>
        <Routes>
          <Route
            index
            element={
              <Dashboard 
                games={games} 
                handleDeleteGame={handleDeleteGame} 
              />
            }
          />
          <Route path="/games/:id" element={<GameDetail onGameUpdate={handleUpdateGame}/>} />
          <Route
            path="/games/new/*"
            element={<GameForm onGameRequest={handleAddGame} />}
          />
        </Routes>
      </main>
      <footer></footer>
    </div>
  );
}

export default App;
