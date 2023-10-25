// TODO: Handle expired tokens with redirects to login page

export const registerFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return fetch("/register", config);
};

export const loginFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  return fetch("/login", config);
};

export const logoutFetch = async () => {
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  };
  return fetch("/logout", config);
};

export const refreshFetch = async () => {
  return fetch("/refresh");
};
