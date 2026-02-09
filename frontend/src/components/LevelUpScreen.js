import React, { useState, useEffect } from "react";
import "./LevelUpScreen.css";

function LevelUpScreen({ newLevel, statIncreases, newStats, onContinue }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    // Trigger animation on mount
    setTimeout(() => setAnimate(true), 100);
  }, []);

  const statsList = [
    { name: "HP", emoji: "❤️" },
    { name: "Mana", emoji: "💎" },
    { name: "Strength", emoji: "💪" },
    { name: "Defense", emoji: "🛡️" },
    { name: "Magic", emoji: "✨" },
    { name: "Dexterity", emoji: "🎯" },
    { name: "Speed", emoji: "⚡" },
    { name: "Swim", emoji: "🌊" },
    { name: "Intellect", emoji: "🧠" },
  ];

  return (
    <div className={`level-up-overlay ${animate ? "show" : ""}`}>
      <div className={`level-up-container ${animate ? "slide-in" : ""}`}>
        {/* Level Up Text */}
        <div className="level-up-header">
          <h1 className="level-up-title">LEVEL UP!</h1>
          <p className="level-number">Level {newLevel}</p>
        </div>

        {/* Stats Display */}
        <div className="stats-container">
          <div className="stats-grid">
            {statsList.map((stat) => (
              statIncreases[stat.name] > 0 && (
                <div key={stat.name} className="stat-increase">
                  <div className="stat-name">
                    <span className="stat-emoji">{stat.emoji}</span>
                    {stat.name}
                  </div>
                  <div className="stat-values">
                    <span className="old-value">{newStats[stat.name] - statIncreases[stat.name]}</span>
                    <span className="arrow">→</span>
                    <span className="new-value">{newStats[stat.name]}</span>
                  </div>
                  <div className="stat-increase-amount">
                    +{statIncreases[stat.name]}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>

        {/* Continue Button */}
        <button className="level-up-continue-btn" onClick={onContinue}>
          Continue Adventure
        </button>
      </div>
    </div>
  );
}

export default LevelUpScreen;
