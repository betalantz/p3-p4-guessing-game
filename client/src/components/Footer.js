import React, { useState } from "react";
import Hint from "./Hint";

function Footer() {
  const [isShowHint, setIsShowHint] = useState(false);

  return (
    <header>
      <div className="toggle-switch">
        <label>Hint</label>
        <input
          type="checkbox"
          id="toggle-show-hint"
          checked={isShowHint}
          onChange={(e) => setIsShowHint(e.target.checked)}
        />
        <label htmlFor="toggle-show-hint"></label>
        {isShowHint ? <Hint /> : null}
      </div>
    </header>
  );
}

export default Footer;
