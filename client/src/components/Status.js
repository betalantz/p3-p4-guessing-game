import React from "react";

function Status({ status }) {
  if (status === "too low")
    return (
      <span role="img" aria-label="edit">
        Try ⬆️
      </span>
    );
  else if (status === "too high")
    return (
      <span role="img" aria-label="edit">
        Try ⬇️
      </span>
    );
  else if (status === "invalid")
    return (
      <span role="img" aria-label="edit">
        ⛔️
      </span>
    );
  else
    return (
      <span role="img" aria-label="edit">
        ✅
      </span>
    );
}

export default Status;
