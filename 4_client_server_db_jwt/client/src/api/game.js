export const gamesFetch = async () => {
  return fetch("/games");
};

export const newGameFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return fetch("/games", config);
};
