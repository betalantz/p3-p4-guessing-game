import React, { useEffect, useState, useCallback } from "react";
import Header from "./Header";
import Footer from "./Footer";
import GameRoundCard from "./GameRoundCard";
import GameRoundForm from "./GameRoundForm";

function App() {
  const [round, setRound] = useState([]);
  const [rounds, setRounds] = useState([]);
  const [isGameOver, setIsGameOver] = useState(false);

  useEffect(() => {
    const fetchAllRounds = async () => {
      const response = await fetch("/rounds");
      const roundArr = await response.json();
      setRounds(roundArr);
    };
    fetchAllRounds().catch(console.error);
  }, []);

  const fetchNewRound = useCallback(async () => {
    const response = await fetch("/round");
    const roundJSON = await response.json();
    setRound(roundJSON);
  }, []);

  useEffect(() => {
    fetchNewRound().catch(console.error);
  }, [fetchNewRound]);

  function handleRound(playedRound) {
    setRounds([...rounds, playedRound]);
    if (playedRound.status === "correct") {
      setRound(playedRound);
      setIsGameOver(true);
    } else {
      fetchNewRound();
    }
  }

  return (
    <main>
      <Header />
      {isGameOver ? (
        <p>Congratulations, you guessed the secret number {round.guess}!</p>
      ) : (
        <GameRoundForm round={round} onPlayRound={handleRound} />
      )}

      <div className="roundList">
        <ul>
          {rounds.toReversed().map((r, index) => (
            <GameRoundCard key={index} round={r} currentRound={index === 0} />
          ))}
        </ul>
      </div>
      <Footer />
    </main>
  );
}

export default App;
