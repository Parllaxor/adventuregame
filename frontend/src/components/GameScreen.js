import React, { useState, useEffect } from "react";
import "./GameScreen.css";
import LevelUpScreen from "./LevelUpScreen";

function GameScreen({
  gameState,
  stats,
  setStats,
  setGameState,
  setInventory,
  onShowStats,
}) {
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("Loading...");
  const [showLevelUp, setShowLevelUp] = useState(false);
  const [levelUpData, setLevelUpData] = useState(null);

  useEffect(() => {
    // Load first event when component mounts
    triggerEvent();
  }, []);

  const triggerEvent = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/event");
      const data = await response.json();
      setEvent(data);
      setMessage("");
    } catch (error) {
      console.error("Error fetching event:", error);
      setMessage("Error loading event");
    }
    setLoading(false);
  };

  const handleChoice = async (choice) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/choose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          choice: choice,
          event_name: event.event_name,
        }),
      });
      const outcome = await response.json();
      
      // Check if this is a level up
      if (outcome.is_level_up) {
        setLevelUpData(outcome);
        setShowLevelUp(true);
      } else {
        setMessage(outcome.text);
        
        // Refresh stats after choice
        const statsResponse = await fetch("http://localhost:5000/api/game-state");
        const gameData = await statsResponse.json();
        setStats(gameData.stats);
        setGameState(gameData.game_state);
        setInventory(gameData.inventory);

        // Auto-load next event after showing outcome
        setTimeout(() => {
          triggerEvent();
        }, 2000);
      }
    } catch (error) {
      console.error("Error handling choice:", error);
      setMessage("Error processing choice");
    }
    setLoading(false);
  };

  const handleLevelUpContinue = async () => {
    setShowLevelUp(false);
    setMessage(levelUpData.text);
    
    // Refresh stats after level up
    const statsResponse = await fetch("http://localhost:5000/api/game-state");
    const gameData = await statsResponse.json();
    setStats(gameData.stats);
    setGameState(gameData.game_state);
    setInventory(gameData.inventory);

    // Auto-load next event after short delay
    setTimeout(() => {
      triggerEvent();
    }, 2000);
  };

  return (
    <div className="game-screen">
      {/* Level Up Screen */}
      {showLevelUp && levelUpData && (
        <LevelUpScreen
          newLevel={levelUpData.new_level}
          statIncreases={levelUpData.stat_increases}
          newStats={levelUpData.new_stats}
          onContinue={handleLevelUpContinue}
        />
      )}

      <div className="game-content">
        {/* Stats Bar */}
        <div className="stats-bar">
          <div className="stat-badge">
            <span className="stat-emoji">⭐</span>
            <span className="stat-label">Lvl</span>
            <span className="stat-val">{stats.Level}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">💎</span>
            <span className="stat-label">XP</span>
            <span className="stat-val">{stats.XP}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">❤️</span>
            <span className="stat-label">HP</span>
            <span className="stat-val">{stats.HP}/{stats.max_HP}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">⚡</span>
            <span className="stat-label">Mana</span>
            <span className="stat-val">{stats.Mana}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">🎯</span>
            <span className="stat-label">Dex</span>
            <span className="stat-val">{stats.Dexterity}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">⚡</span>
            <span className="stat-label">Spd</span>
            <span className="stat-val">{stats.Speed}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">🌊</span>
            <span className="stat-label">Swim</span>
            <span className="stat-val">{stats.Swim}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">🧠</span>
            <span className="stat-label">Int</span>
            <span className="stat-val">{stats.Intellect}</span>
          </div>

          <button className="mini-btn" onClick={onShowStats}>
            Full Stats
          </button>
        </div>

        {/* Event Display */}
        <div className="event-box">
          {message ? (
            <div className="message-display">
              <p>{message}</p>
            </div>
          ) : event ? (
            <div className="event-display">
              <h2>{event.event_name.replace("trigger_", "").toUpperCase()}</h2>
              <p className="event-text">{event.text}</p>
            </div>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* Choice Buttons */}
        {!message && event && (
          <div className="choices">
            {event.choices.map((choice, idx) => (
              <button
                key={idx}
                className="choice-btn"
                onClick={() => handleChoice(choice)}
                disabled={loading}
              >
                {choice}
              </button>
            ))}
          </div>
        )}

        {/* Continue Button after message */}
        {message && (
          <div className="choices">
            <button className="choice-btn" onClick={triggerEvent} disabled={loading}>
              Continue...
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default GameScreen;
