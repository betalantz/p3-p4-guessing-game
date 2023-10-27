// a helper function to navigate to the login page
// a workaround to allow navigation from outside the RouterProvider

let navigate = null;

export function setNavigate(n) {
  navigate = n;
}

export function goToLogin() {
  if (navigate) {
    navigate('/login');
  }
}