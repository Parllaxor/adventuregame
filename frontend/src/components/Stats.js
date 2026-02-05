import React from "react";
import "./Stats.css";

function Stats({ stats, inventory, onBack }) {
  return (
    <div className="stats-screen">
      <div className="stats-container">
        <button className="back-btn" onClick={onBack}>
          ← Back to Game
        </button>

        <h1>Character Stats & Inventory</h1>

        <div className="stats-grid">
          <div className="stats-column">
            <h2>Stats</h2>
            <div className="stat-row">
              <span>HP:</span>
              <span className="stat-value">
                {stats.HP}/{stats.max_HP}
              </span>
            </div>
            <div className="stat-row">
              <span>Mana:</span>
              <span className="stat-value">{stats.Mana}</span>
            </div>
            <div className="stat-row">
              <span>Energy:</span>
              <span className="stat-value">{stats.Energy}</span>
            </div>
            <div className="stat-row">
              <span>Strength:</span>
              <span className="stat-value">{stats.Strength}</span>
            </div>
            <div className="stat-row">
              <span>Defense:</span>
              <span className="stat-value">{stats.Defense}</span>
            </div>
            <div className="stat-row">
              <span>Magic:</span>
              <span className="stat-value">{stats.Magic}</span>
            </div>
            <div className="stat-row highlight">
              <span>XP:</span>
              <span className="stat-value">{stats.XP}</span>
            </div>
            <div className="stat-row highlight">
              <span>Level:</span>
              <span className="stat-value">{stats.Level}</span>
            </div>
          </div>

          <div className="stats-column">
            <h2>Inventory</h2>
            {Object.entries(inventory).map(([item, count]) => (
              <div key={item} className="stat-row">
                <span>{item}:</span>
                <span className="stat-value">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Stats;
