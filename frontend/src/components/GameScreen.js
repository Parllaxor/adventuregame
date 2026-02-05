import React, { useState, useEffect } from "react";
import "./GameScreen.css";

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
    } catch (error) {
      console.error("Error handling choice:", error);
      setMessage("Error processing choice");
    }
    setLoading(false);
  };

  return (
    <div className="game-screen">
      <div className="game-content">
        {/* Stats Bar */}
        <div className="stats-bar">
          <div className="stat">❤️ HP: {stats.HP}/{stats.max_HP}</div>
          <div className="stat">💎 XP: {stats.XP}</div>
          <div className="stat">⚡ Mana: {stats.Mana}</div>
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
