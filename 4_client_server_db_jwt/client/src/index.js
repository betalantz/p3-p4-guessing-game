import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import AuthProvider from "./providers/authProvider";
import "./index.css";
import App from "./App";
const root = document.getElementById("root");

createRoot(root).render(
  // <BrowserRouter>
  <AuthProvider>
    <App />
  </AuthProvider>
  // </BrowserRouter>
);
