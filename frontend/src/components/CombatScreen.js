import React, { useState, useEffect } from "react";
import "./GameScreen.css";

function CombatScreen({
  combatState,
  stats,
  equipment,
  availableWeapons,
  availableSpells,
  onAttack,
  onEquipWeapon,
  onEquipSpell,
  loading,
}) {
  const [selectedWeapon, setSelectedWeapon] = useState(equipment.weapon || "Fist");
  const [selectedSpell, setSelectedSpell] = useState(equipment.spell || null);
  const [combatLog, setCombatLog] = useState([]);

  useEffect(() => {
    // Add new combat messages to log
    if (combatState.log) {
      setCombatLog((prev) => [...prev, combatState.log]);
    }
  }, [combatState.log]);

  const handleWeaponChange = async (weapon) => {
    setSelectedWeapon(weapon);
    await onEquipWeapon(weapon);
  };

  const handleSpellChange = async (spell) => {
    setSelectedSpell(spell);
    await onEquipSpell(spell);
  };

  const handleAttack = async (type) => {
    const actionName = type === "weapon" ? selectedWeapon : selectedSpell;
    await onAttack(type, actionName);
  };

  const getHPPercentage = () => {
    if (!stats) return 0;
    return (stats.HP / stats.max_HP) * 100;
  };

  const getEnemyHPPercentage = () => {
    if (combatState.enemyMaxHp === 0) return 0;
    return (combatState.enemyHp / combatState.enemyMaxHp) * 100;
  };

  const getManaPercentage = () => {
    if (!stats) return 0;
    return (stats.Mana / stats.max_Mana) * 100;
  };

  return (
    <div className="combat-screen">
      <div className="combat-header">
        <h2>⚔️ Combat</h2>
      </div>

      <div className="combat-area">
        <div className="player-section">
          <div className="character-status">
            <h3>Your HP</h3>
            <div className="hp-bar">
              <div
                className="hp-fill"
                style={{ width: `${getHPPercentage()}%` }}
              ></div>
            </div>
            <p>
              {stats?.HP || 0} / {stats?.max_HP || 0}
            </p>

            <h3>Mana</h3>
            <div className="mana-bar">
              <div
                className="mana-fill"
                style={{ width: `${getManaPercentage()}%` }}
              ></div>
            </div>
            <p>
              {stats?.Mana || 0} / {stats?.max_Mana || 0}
            </p>
          </div>
        </div>

        <div className="enemy-section">
          <div className="character-status">
            <h3>{combatState.enemy}</h3>
            <div className="hp-bar">
              <div
                className="hp-fill enemy"
                style={{ width: `${getEnemyHPPercentage()}%` }}
              ></div>
            </div>
            <p>
              {combatState.enemyHp || 0} / {combatState.enemyMaxHp || 0}
            </p>
          </div>
        </div>
      </div>

      <div className="combat-log-display">
        <h4>Combat Log</h4>
        <div className="combat-log">
          {combatState.log && (
            <p className="log-entry">{combatState.log}</p>
          )}
          {combatLog.map((entry, idx) => (
            <p key={idx} className="log-entry">
              {entry}
            </p>
          ))}
        </div>
      </div>

      <div className="combat-actions">
        <div className="weapon-section">
          <h4>Weapons</h4>
          <div className="weapon-buttons">
            {availableWeapons && availableWeapons.length > 0 ? (
              availableWeapons.map((weapon) => (
                <button
                  key={weapon}
                  className={`weapon-btn ${
                    selectedWeapon === weapon ? "selected" : ""
                  }`}
                  onClick={() => handleWeaponChange(weapon)}
                  disabled={loading}
                >
                  {weapon}
                </button>
              ))
            ) : (
              <p>No weapons available</p>
            )}
          </div>
          <button
            className="attack-btn weapon-attack"
            onClick={() => handleAttack("weapon")}
            disabled={loading || !selectedWeapon}
          >
            🗡️ Attack
          </button>
        </div>

        <div className="spell-section">
          <h4>Spells</h4>
          <div className="spell-buttons">
            {availableSpells && availableSpells.length > 0 ? (
              availableSpells.map((spell) => (
                <button
                  key={spell}
                  className={`spell-btn ${
                    selectedSpell === spell ? "selected" : ""
                  }`}
                  onClick={() => handleSpellChange(spell)}
                  disabled={loading}
                >
                  {spell}
                </button>
              ))
            ) : (
              <p>No spells available</p>
            )}
          </div>
          <button
            className="attack-btn spell-attack"
            onClick={() => handleAttack("spell")}
            disabled={loading || !selectedSpell}
          >
            ✨ Cast Spell
          </button>
        </div>
      </div>
    </div>
  );
}

export default CombatScreen;
