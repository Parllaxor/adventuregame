import React, { useState, useEffect, useRef } from "react";
import "./GameScreen.css";
import LevelUpScreen from "./LevelUpScreen";
import CombatScreen from "./CombatScreen";

function GameScreen({
  gameState,
  stats,
  setStats,
  setGameState,
  setInventory,
  onShowStats,
}) {
  const [transitionLock, setTransitionLock] = useState(false);
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
    availableWeapons: [],
    availableSpells: [],
    combatLog: [],
  });

  const [equipment, setEquipment] = useState({
    weapon: "Fist",
    spell: null,
  });

  const [availableGear, setAvailableGear] = useState({
    weapons: [],
    spells: [],
  });

  const [bowlingState, setBowlingState] = useState({
    active: false,
    score: 0,
    rolls: 0,
    rollsRemaining: 5,
    lastRoll: null,
    rollHistory: [],
  });

  // The main gameplay screen switches between event, combat, and minigame modes.
  // Add new modes here if a new interaction type should be handled separately.
  const [mode, setMode] = useState("event");

  const modeRef = useRef(mode);

  useEffect(() => {
    modeRef.current = mode;
  }, [mode]);

  useEffect(() => {
    if (transitionLock) return;

    if (modeRef.current === "event" && !event && !loading && !message) {
      triggerEvent();
    }
  }, [mode, event, loading, transitionLock, message]);

  useEffect(() => {
    if (mode === "event" && !loading) {
      setTransitionLock(false);
    }
  }, [mode, loading]);

  // Syncs the UI with the backend after events, combat, or inventory changes.
  // If you add new state that should always reflect the server, update this helper.
  const syncGameData = async () => {
    if (modeRef.current === "bowling") return;

    const statsResponse = await fetch("http://localhost:5000/api/game-state");
    const gameData = await statsResponse.json();

    setStats(gameData.stats);
    setGameState(gameData.game_state);
    setInventory(gameData.inventory);

    setEquipment({
      weapon: gameData.equipped_weapon || "Fist",
      spell: gameData.equipped_spell || null,
    });

    setAvailableGear({
      weapons: Object.keys(gameData.weapons || {}),
      spells: Object.keys(gameData.spells || {}),
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

  const formatEventName = (name) => {
    return name
      .replace(/^trigger_/, "")
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const triggerEvent = async () => {
    if (loading) return;

    console.trace("triggerEvent called");
    if (modeRef.current !== "event") return;

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/event");
      const data = await response.json();

      if (modeRef.current !== "event") return;

      setEvent(data);
      setMessage("");
      await syncGameData();
    } catch (error) {
      setMessage("Error loading event");
    } finally {
      setLoading(false);
    }
  };

  // This is the main action pipeline for event choices. New event outcomes should be
  // handled here or by the backend response that the UI receives.
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

      if (outcome.minigame === "bowling") {
        setTransitionLock(true);
        setMode("bowling");

        setBowlingState({
          active: true,
          score: 0,
          rolls: 0,
          rollsRemaining: 5,
          lastRoll: null,
          rollHistory: [],
        });

        setEvent(null);
        setMessage("");
        setLoading(false);
        return;
      }

      const gameData = await syncGameData();

      if (outcome.is_level_up) {
        setLevelUpData(outcome);
        setShowLevelUp(true);
      }

      if (outcome.battle_started || outcome.combat_active) {
        setCombatState({
          active: true,
          enemy: outcome.enemy || gameData.game_state?.current_enemy || "Enemy",
          enemyHp: outcome.enemy_hp ?? 0,
          enemyMaxHp: outcome.enemy_max_hp ?? 0,
          log: outcome.text || "Combat started!",
          availableWeapons: outcome.available_weapons || [],
          availableSpells: outcome.available_spells || [],
          combatLog: outcome.combat_log || [],
        });
        setMode("combat");
        setEvent(null);
        setMessage("");
        return;
      }

      if (
        Array.isArray(outcome.choices) &&
        outcome.choices.length > 0 &&
        outcome.continue === false
      ) {
        setEvent(outcome);
        setMessage("");
        return;
      }

      setMessage(outcome.text || "Action complete.");
      setEvent(null);
    } catch (err) {
      console.error("Error:", err);
      setMessage("Error processing choice");
    } finally {
      setLoading(false);
    }
  };

  const handleCombatAttack = async (type, actionName) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/combat-attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: type,
          action: actionName,
        }),
      });

      const result = await response.json();

      if (result.error) {
        setCombatState((prev) => ({
          ...prev,
          log: `❌ Error: ${result.error}`,
        }));
        return;
      }

      // Update combat state
      setCombatState((prev) => ({
        ...prev,
        enemy: result.enemy,
        enemyHp: result.enemy_hp,
        enemyMaxHp: result.enemy_max_hp,
        log: result.combat_log ? result.combat_log.join("\n") : "",
        combatLog: result.combat_log || [],
        active: result.combat_active,
      }));

      // Update player stats
      if (result.player_hp !== undefined) {
        setStats((prev) => ({
          ...prev,
          HP: result.player_hp,
          Mana: result.player_mana,
        }));
      }

      // Handle combat end
      if (result.combat_end) {
        setTimeout(() => {
          if (result.game_over) {
            setMessage("💀 Game Over. You have been defeated...");
            setMode("event");
          } else {
            setMessage(result.end_message);
            setCombatState((prev) => ({
              ...prev,
              active: false,
            }));
            setMode("event");
          }
        }, 1500);
      }

      // Handle level up
      if (result.is_level_up) {
        setLevelUpData(result);
        setShowLevelUp(true);
      }
    } catch (err) {
      console.error("Combat error:", err);
      setCombatState((prev) => ({
        ...prev,
        log: "❌ Error during combat. Please try again.",
      }));
    } finally {
      setLoading(false);
    }
  };

  const handleEquipWeapon = async (weaponName) => {
    try {
      const response = await fetch("http://localhost:5000/api/equip-weapon", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ weapon: weaponName }),
      });

      const result = await response.json();
      if (result.success) {
        setEquipment((prev) => ({
          ...prev,
          weapon: result.equipped_weapon,
        }));
      }
    } catch (err) {
      console.error("Equip error:", err);
    }
  };

  const handleEquipSpell = async (spellName) => {
    try {
      const response = await fetch("http://localhost:5000/api/equip-spell", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ spell: spellName }),
      });

      const result = await response.json();
      if (result.success) {
        setEquipment((prev) => ({
          ...prev,
          spell: result.equipped_spell,
        }));
      }
    } catch (err) {
      console.error("Equip error:", err);
    }
  };

  const endBowlingGame = async () => {
    const finalScore = bowlingState.score;

    await fetch("http://localhost:5000/api/end-minigame", {
      method: "POST",
    });

    setStats((prev) => ({
      ...prev,
      XP: prev.XP + finalScore,
    }));

    setBowlingState({
      active: false,
      score: 0,
      rolls: 0,
      rollsRemaining: 5,
      lastRoll: null,
      rollHistory: [],
    });

    setMode("event");

    setMessage(`Bowling complete, Score: ${finalScore}`);
  };

  const rollBowlingBall = () => {
    setBowlingState((prev) => {
      if (!prev.active || prev.rollsRemaining <= 0) {
        return prev;
      }

      const knockedDown = Math.floor(Math.random() * 10) + 1;
      return {
        ...prev,
        score: prev.score + knockedDown,
        rolls: prev.rolls + 1,
        rollsRemaining: prev.rollsRemaining - 1,
        lastRoll: knockedDown,
        rollHistory: [...prev.rollHistory, knockedDown],
      };
    });
  };

  const renderContent = () => {
    if (bowlingState.active) {
      return (
        <div className="event-display">
          <h2>🎳 Bowling</h2>
          <p>Score: {bowlingState.score}</p>
          <p>Rolls: {bowlingState.rolls} / 5</p>
          {bowlingState.lastRoll !== null && (
            <p>Last roll: {bowlingState.lastRoll} pins</p>
          )}
          <p>
            {bowlingState.rollsRemaining > 0
              ? `Roll the ball and knock down as many pins as you can.`
              : "No rolls left. Finish your game to collect XP."}
          </p>

          <button
            className="choice-btn"
            onClick={rollBowlingBall}
            disabled={bowlingState.rollsRemaining <= 0}
          >
            Roll Ball
          </button>

          <button className="choice-btn" onClick={endBowlingGame}>
            Finish
          </button>

          {bowlingState.rollHistory.length > 0 && (
            <div className="bowling-history">
              <h4>Roll history</h4>
              <p>{bowlingState.rollHistory.join(" - ")}</p>
            </div>
          )}
        </div>
      );
    }

    if (combatState.active) {
      return (
        <CombatScreen
          combatState={combatState}
          stats={stats}
          equipment={equipment}
          availableWeapons={combatState.availableWeapons}
          availableSpells={combatState.availableSpells}
          onAttack={handleCombatAttack}
          onEquipWeapon={handleEquipWeapon}
          onEquipSpell={handleEquipSpell}
          loading={loading}
        />
      );
    }

    if (loading && !event) {
      return <p>Loading...</p>;
    }

    if (message) {
      return (
        <div className="message-display">
          <p>{message}</p>
          <button
            className="choice-btn"
            onClick={triggerEvent}
            disabled={loading}
          >
            Continue
          </button>
        </div>
      );
    }

    if (event) {
      return (
        <div className="event-display">
          <h2>{formatEventName(event.event_name)}</h2>
          <p>{event.text}</p>
          {Array.isArray(event.choices) && event.choices.length > 0 && (
            <div className="choices">
              {event.choices.map((choice, index) => (
                <button
                  key={index}
                  className="choice-btn"
                  onClick={() => handleChoice(choice)}
                  disabled={loading}
                >
                  {choice}
                </button>
              ))}
            </div>
          )}
        </div>
      );
    }

    return <p>Loading...</p>;
  };

  const renderEquipPanel = () => {
    if (combatState.active || mode === "bowling") return null;

    const hasWeapons = availableGear.weapons.length > 0;
    const hasSpells = availableGear.spells.length > 0;
    if (!hasWeapons && !hasSpells) return null;

    return (
      <div className="equip-panel">
        <h4>Equip on Main Screen</h4>
        <div className="equip-row">
          {hasWeapons && (
            <div className="equip-group">
              <label htmlFor="weapon-select">Weapon</label>
              <select
                id="weapon-select"
                value={equipment.weapon || "Fist"}
                onChange={(e) => handleEquipWeapon(e.target.value)}
                disabled={loading}
                className="equip-select"
              >
                {availableGear.weapons.map((weapon) => (
                  <option key={weapon} value={weapon}>
                    {weapon}
                  </option>
                ))}
              </select>
            </div>
          )}
          {hasSpells && (
            <div className="equip-group">
              <label htmlFor="spell-select">Spell</label>
              <select
                id="spell-select"
                value={equipment.spell || ""}
                onChange={(e) => handleEquipSpell(e.target.value || null)}
                disabled={loading}
                className="equip-select"
              >
                <option value="">None</option>
                {availableGear.spells.map((spell) => (
                  <option key={spell} value={spell}>
                    {spell}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="game-screen">
      <div className="game-content">
        <div className="event-box">{renderContent()}</div>
        {renderEquipPanel()}
      </div>
      {showLevelUp && levelUpData && (
        <LevelUpScreen
          levelUpData={levelUpData}
          onClose={() => setShowLevelUp(false)}
        />
      )}
    </div>
  );
}

export default GameScreen;
