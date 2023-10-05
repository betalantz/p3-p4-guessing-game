import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import GameDetail from "./components/GameDetail";
import AuthProvider from './providers/authProvider'

function App() {
  return (
    <div>
      <AuthProvider>
        <Header />
        <main>
          <Routes>
            <Route index element={<Dashboard />} />
            <Route path="/games/:id/*" element={<GameDetail />} />
          </Routes>
        </main>
        <footer></footer>
      </AuthProvider>
    </div>
  );
}

export default App;
