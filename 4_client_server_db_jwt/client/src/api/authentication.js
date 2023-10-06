export const registerFetch = async (formData) => {
  const config = {
    method: "POST",
    body: JSON.stringify(formData),
    headers: {
      "Content-Type": "application/json",
    },
  };
  const response = await fetch("/register", config);
  return response
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
 return response
};
