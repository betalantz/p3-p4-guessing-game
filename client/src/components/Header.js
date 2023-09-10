import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <nav>
      <span>
        <h1>
          <Link to="/">Guess the number</Link>
        </h1>
      </span>
    </nav>
  );
}

export default Header;
