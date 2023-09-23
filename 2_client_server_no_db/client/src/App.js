import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import GameDetail from "./components/GameDetail";

function App() {
  return (
    <div>
      <Header />
      <main>
        <Routes>
          <Route index element={<Dashboard />} />
          <Route path="/games/:id/*" element={<GameDetail />} />
        </Routes>
      </main>
      <footer></footer>
    </div>
  );
}

export default App;
