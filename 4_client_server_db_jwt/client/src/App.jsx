import React from "react";
// import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import GameDetail from "./components/GameDetail";
import { useAuth } from './providers/authProvider'
import Routes from './routes/Routes'
import NavMenu from "./components/NavMenu";

function App() {

  const { token } = useAuth();

  return (
    <div>
        {/* <Header /> */}
        <main>
          <Routes>
            {/* <Route index element={<Dashboard />} />
            <Route path="/games/:id/*" element={<GameDetail />} /> */}
          </Routes>
        </main>
        <footer></footer>
    </div>
  );
}

export default App;
