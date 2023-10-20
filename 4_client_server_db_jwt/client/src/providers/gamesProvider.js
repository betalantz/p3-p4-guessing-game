import { createContext, useContext, useMemo, useState } from "react";

const GamesContext = createContext();

const GamesProvider = ({ children }) => {
  const [games, setGames_] = useState([]);

  const contextValue = useMemo(() => {
    const setGames = (newGames) => setGames_(newGames);
    return { games, setGames };
  }, [games]);

  return (
    <GamesContext.Provider value={contextValue}>{children}</GamesContext.Provider>
  );
}

export const useGames = () => useContext(GamesContext);

export default GamesProvider;