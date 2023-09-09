import React, { useEffect, useState, useCallback } from "react";

function Hint() {
  const [hintMessage, setHintMessage] = useState();

  const fetchHint = useCallback(async () => {
    const response = await fetch("/hint");
    const hintJson = await response.json();
    setHintMessage(hintJson["hint"]);
  }, []);

  useEffect(() => {
    fetchHint().catch(console.error);
  }, [fetchHint]);

  return <span>{hintMessage}</span>;
}

export default Hint;
