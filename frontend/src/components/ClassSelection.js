import React from "react";
import "./ClassSelection.css";

function ClassSelection({ onSelectClass }) {
  return (
    <div className="class-selection">
      <div className="class-container">
        <h1>Welcome to Adventure Game!</h1>
        <p>Choose your character class:</p>

        <div className="class-buttons">
          <button
            className="class-btn warrior-btn"
            onClick={() => onSelectClass(1)}
          >
            <span className="class-name">⚔️ Warrior</span>
            <span className="class-desc">+5 Strength, +3 Defense</span>
          </button>

          <button
            className="class-btn mage-btn"
            onClick={() => onSelectClass(2)}
          >
            <span className="class-name">🔮 Mage</span>
            <span className="class-desc">+5 Magic, +3 Intellect</span>
          </button>

          <button
            className="class-btn defender-btn"
            onClick={() => onSelectClass(3)}
          >
            <span className="class-name">🛡️ Defender</span>
            <span className="class-desc">+5 Defense, +3 Strength</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default ClassSelection;
