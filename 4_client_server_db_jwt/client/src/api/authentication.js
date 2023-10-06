export const registerFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await fetch("/register", config);
  const messageJSON = await response.json();
  return messageJSON;
};

export const loginFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await fetch("/login", config);
  const tokenJSON = await response.json();
  return tokenJSON;
};
