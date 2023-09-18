import React from "react";

function Status({ status }) {
  console.log(status);
  if (status === "Status.LOW")
    return (
      <span role="img" aria-label="edit">
        Try ⬆️
      </span>
    );
  else if (status === "Status.HIGH")
    return (
      <span role="img" aria-label="edit">
        Try ⬇️
      </span>
    );
  else if (status === "Status.INVALID")
    return (
      <span role="img" aria-label="edit">
        ⛔️
      </span>
    );
  else if (status === "Status.CORRECT")
    return (
      <span role="img" aria-label="edit">
        ✅
      </span>
    );
  else return <span></span>;
}

export default Status;
