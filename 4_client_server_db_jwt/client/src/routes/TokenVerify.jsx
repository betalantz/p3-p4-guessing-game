import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, Outlet } from "react-router-dom";
import { useAuth } from "../providers/authProvider";
import StatusDetail from "../components/StatusDetail";
import { logoutFetch } from "../api";

function TokenVerify() {
  const [message, setMessage] = useState("");

  const { isTokenExpired } = useAuth();

  const location = useLocation();

  const navigate = useNavigate();

  // If the token is expired, set a message and log the user out after 10 seconds.
  // Extensible to show a modal to the user to ask if they want to stay logged in, display countdown, etc.
  useEffect(() => {
    if (isTokenExpired()) {
      setMessage({
        message: "You will be logged out in 10 seconds due to inactivity.",
      });
      setTimeout(async () => {
        const res = await logoutFetch();
        if (res.ok) {
          setMessage("");
          navigate("/login");
        } else {
          setMessage("Logout failed.");
        }
      }, 10000);
    }
  }, [location, navigate, isTokenExpired]);

  return (
    <>
      {message && (
        <StatusDetail
          message={message}
          isError={true}
          onCloseHandler={() => setMessage("")}
        />
      )}
      <Outlet />
    </>
  );
}

export default TokenVerify;
