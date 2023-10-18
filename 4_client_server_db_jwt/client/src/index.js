import React from "react";
import { createRoot } from "react-dom/client";
import AuthProvider from "./providers/authProvider";
import "./index.css";
import App from "./App";
const root = document.getElementById("root");

createRoot(root).render(
  <AuthProvider>
    <App />
  </AuthProvider>
);
