import { createContext, useContext, useMemo, useState } from "react";

const GamesContext = createContext();

const GamesProvider = ({ children }) => {
  const [games, setGames_] = useState([]);
  const [rounds, setRounds_] = useState([]);

  const contextValue = useMemo(() => {
    const setGames = (newGames) => setGames_(newGames);
    const setRounds = (newRounds) => setRounds_(newRounds)
    return { games, setGames, rounds, setRounds };
  }, [games, rounds]);

  return (
    <GamesContext.Provider value={contextValue}>{children}</GamesContext.Provider>
  );
}

export const useGames = () => useContext(GamesContext);

export default GamesProvider;