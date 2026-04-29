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
  const [combatState, setCombatState] = useState({
    active: false,
    enemy: null,
    enemyHp: 0,
    enemyMaxHp: 0,
    log: "",
  });
  const [equipment, setEquipment] = useState({
    weapon: "Fist",
    spell: null,
  });

  useEffect(() => {
    triggerEvent();
  }, []);

  const syncGameData = async () => {
    const statsResponse = await fetch("http://localhost:5000/api/game-state");
    const gameData = await statsResponse.json();

    setStats(gameData.stats);
    setGameState(gameData.game_state);
    setInventory(gameData.inventory);
    setEquipment({
      weapon: gameData.equipped_weapon || "Fist",
      spell: gameData.equipped_spell || null,
    });
    setCombatState((prev) => ({
      ...prev,
      active: Boolean(gameData.game_state?.in_combat),
      enemy: gameData.game_state?.current_enemy || prev.enemy || null,
      enemyHp: gameData.game_state?.current_enemy_hp ?? prev.enemyHp ?? 0,
      enemyMaxHp:
        gameData.game_state?.current_enemy_max_hp ??
        prev.enemyMaxHp ??
        prev.enemyHp ??
        0,
    }));

    return gameData;
  };

  const triggerEvent = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/event");
      const data = await response.json();
      setEvent(data);
      setMessage("");
      await syncGameData();
    } catch (error) {
      console.error("Error fetching event:", error);
      setMessage("Error loading event");
    } finally {
      setLoading(false);
    }
  };

  const handleChoice = async (choice) => {
    if (!event) return;

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/choose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          choice,
          event_name: event.event_name,
        }),
      });
      const outcome = await response.json();
      const gameData = await syncGameData();

      if (outcome.is_level_up) {
        setLevelUpData(outcome);
        setShowLevelUp(true);
      }

      if (outcome.battle_started || outcome.combat_active) {
        setCombatState({
          active: true,
          enemy: outcome.enemy || gameData.game_state?.current_enemy || "Enemy",
          enemyHp: outcome.enemy_hp ?? gameData.game_state?.current_enemy_hp ?? 0,
          enemyMaxHp:
            outcome.enemy_max_hp ??
            gameData.game_state?.current_enemy_max_hp ??
            outcome.enemy_hp ??
            0,
          log: outcome.text || outcome.message || "Combat started!",
        });
        setEvent(null);
        setMessage("");
        return;
      }

      if (
        Array.isArray(outcome.choices) &&
        outcome.choices.length > 0 &&
        outcome.continue === false
      ) {
        setEvent({
          ...outcome,
          event_name: outcome.event_name || "encounter",
        });
        setMessage("");
        return;
      }

      setMessage(outcome.text || "Action complete.");
      setEvent(null);
    } catch (error) {
      console.error("Error handling choice:", error);
      setMessage("Error processing choice");
    } finally {
      setLoading(false);
    }
  };

  const handleCombatAction = async (type) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/combat-attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type,
          action: "equipped",
        }),
      });
      const outcome = await response.json();
      const gameData = await syncGameData();

      if (!response.ok || outcome.error) {
        setCombatState((prev) => ({
          ...prev,
          log: outcome.error || "Combat action failed.",
        }));
        return;
      }

      if (outcome.is_level_up) {
        setLevelUpData({
          ...outcome,
          text: [outcome.action_text, outcome.end_message].filter(Boolean).join("\n"),
        });
        setShowLevelUp(true);
      }

      if (outcome.combat_end || !outcome.combat_active) {
        setCombatState({
          active: false,
          enemy: null,
          enemyHp: 0,
          enemyMaxHp: 0,
          log: "",
        });
        setMessage(
          [outcome.action_text, outcome.end_message].filter(Boolean).join("\n") ||
            "Combat ended."
        );
        setEvent(null);
        return;
      }

      setCombatState({
        active: true,
        enemy: outcome.enemy || gameData.game_state?.current_enemy || "Enemy",
        enemyHp: outcome.enemy_hp ?? gameData.game_state?.current_enemy_hp ?? 0,
        enemyMaxHp:
          outcome.enemy_max_hp ??
          gameData.game_state?.current_enemy_max_hp ??
          combatState.enemyMaxHp ??
          0,
        log: outcome.action_text || "Attack resolved.",
      });
      setMessage("");
    } catch (error) {
      console.error("Error during combat:", error);
      setCombatState((prev) => ({
        ...prev,
        log: "Error during combat action.",
      }));
    } finally {
      setLoading(false);
    }
  };

  const handleLevelUpContinue = async () => {
    setShowLevelUp(false);
    const combinedMessage = [levelUpData?.text, levelUpData?.level_up_text]
      .filter(Boolean)
      .join("\n\n");

    if (combinedMessage) {
      setMessage(combinedMessage);
    }

    await syncGameData();
  };

  const eventTitle = combatState.active
    ? `⚔️ ${String(combatState.enemy || "Enemy").toUpperCase()}`
    : event?.event_name
      ? event.event_name.replace("trigger_", "").replace(/_/g, " ").toUpperCase()
      : "ADVENTURE";

  return (
    <div className="game-screen">
      {showLevelUp && levelUpData && (
        <LevelUpScreen
          newLevel={levelUpData.new_level}
          statIncreases={levelUpData.stat_increases}
          newStats={levelUpData.new_stats}
          onContinue={handleLevelUpContinue}
        />
      )}

      <div className="game-content">
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
            <span className="stat-emoji">🔷</span>
            <span className="stat-label">Mana</span>
            <span className="stat-val">{stats.Mana}/{stats.max_Mana ?? stats.Mana}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">💪</span>
            <span className="stat-label">Str</span>
            <span className="stat-val">{stats.Strength}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">🛡️</span>
            <span className="stat-label">Def</span>
            <span className="stat-val">{stats.Defense}</span>
          </div>

          <div className="stat-badge">
            <span className="stat-emoji">✨</span>
            <span className="stat-label">Mag</span>
            <span className="stat-val">{stats.Magic}</span>
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

        <div className="event-box">
          {combatState.active ? (
            <div className="event-display combat-display">
              <h2>{eventTitle}</h2>
              <p className="event-text enemy-health">
                Enemy HP: {combatState.enemyHp}/{combatState.enemyMaxHp}
              </p>
              <p className="event-text combat-log">{combatState.log}</p>
            </div>
          ) : message ? (
            <div className="message-display">
              <p>{message}</p>
            </div>
          ) : event ? (
            <div className="event-display">
              <h2>{eventTitle}</h2>
              <p className="event-text">{event.text}</p>
            </div>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {combatState.active ? (
          <div className="choices combat-actions">
            <button
              className="choice-btn"
              onClick={() => handleCombatAction("weapon")}
              disabled={loading}
            >
              ⚔️ Attack with {equipment.weapon}
            </button>

            {equipment.spell && (
              <button
                className="choice-btn"
                onClick={() => handleCombatAction("spell")}
                disabled={loading}
              >
                ✨ Cast {equipment.spell}
              </button>
            )}
          </div>
        ) : !message && event && Array.isArray(event.choices) ? (
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
        ) : null}

        {message && !combatState.active && (
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
