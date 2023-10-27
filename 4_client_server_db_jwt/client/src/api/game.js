export const gamesFetch = async () => {
  return fetch("/games");
};

// export const gamesByIdFetch = async (id) => {
//   return fetch(`/games/${id}`);
// };

export const deleteGamesByIdFetch = async (id) => {
  return fetch(`/games/${id}`);
};

export const postGamesFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return fetch("/games", config);
};

export const patchGamesFetch = async (formData, round) => {
  const config = {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  };
  return fetch(`/games/${round.game_id}/rounds`, config);
};

export const roundsByGameIdFetch = async (id) => {
  return fetch(`/games/${id}/rounds`);
};

