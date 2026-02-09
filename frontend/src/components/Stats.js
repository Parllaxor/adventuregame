import React, { useEffect, useState } from "react";
import "./Stats.css";

function Stats({ stats, inventory, onBack }) {
  const [inv, setInv] = useState(inventory || {});
  const [weapons, setWeapons] = useState({});
  const [spells, setSpells] = useState({});
  const [equippedWeapon, setEquippedWeapon] = useState(null);
  const [equippedSpell, setEquippedSpell] = useState(null);

  const fetchInventory = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/inventory");
      const data = await res.json();
      console.log("🎒 Inventory fetched:", data);
      setInv(data.resources || {});
      setWeapons(data.weapons || {});
      setSpells(data.spells || {});
      setEquippedWeapon(data.equipped_weapon || null);
      setEquippedSpell(data.equipped_spell || null);
      console.log("   Spells loaded:", data.spells);
      console.log("   Equipped spell:", data.equipped_spell);
    } catch (e) {
      console.error("Failed to fetch inventory", e);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  const equipWeapon = async (w) => {
    try {
      const res = await fetch("http://localhost:5000/api/equip-weapon", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ weapon: w }),
      });
      const data = await res.json();
      if (data.error) {
        console.error("Equip weapon error:", data.error);
        return;
      }
      // Update local state from server response
      setEquippedWeapon(data.equipped || w);
      if (data.weapons) setWeapons(data.weapons);
    } catch (e) {
      console.error(e);
    }
  };

  const equipSpell = async (s) => {
    console.log("equipSpell called with:", s);
    try {
      const payload = { spell: s };
      console.log("Sending payload:", payload);
      const res = await fetch("http://localhost:5000/api/equip-spell", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      console.log("Response status:", res.status);
      const data = await res.json();
      console.log("Response data:", data);
      if (data.error) {
        console.error("Equip spell error:", data.error);
        alert(`Error: ${data.error}`);
        return;
      }
      console.log("Setting equipped spell to:", data.equipped);
      setEquippedSpell(data.equipped);
      if (data.spells) {
        console.log("Updating spells in state:", data.spells);
        setSpells(data.spells);
      }
    } catch (e) {
      console.error("Exception during equipSpell:", e);
    }
  };

  return (
    <div className="stats-screen">
      <div className="stats-container">
        <button className="back-btn" onClick={onBack}>
          ← Back to Game
        </button>

        <h1>Character Stats & Inventory</h1>
        
        {/* DEBUG: Show status */}
        {spells && Object.keys(spells).length > 0 && (
          <div style={{background: '#333', padding: '10px', marginBottom: '10px', borderRadius: '5px', fontSize: '0.9rem'}}>
            📊 Loaded {Object.keys(spells).length} spell(s): {Object.keys(spells).join(', ')} | Equipped: {equippedSpell}
          </div>
        )}

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
            <div className="stat-row">
              <span>Dexterity:</span>
              <span className="stat-value">{stats.Dexterity}</span>
            </div>
            <div className="stat-row">
              <span>Speed:</span>
              <span className="stat-value">{stats.Speed}</span>
            </div>
            <div className="stat-row">
              <span>Swim:</span>
              <span className="stat-value">{stats.Swim}</span>
            </div>
            <div className="stat-row">
              <span>Intellect:</span>
              <span className="stat-value">{stats.Intellect}</span>
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
            {Object.entries(inv).map(([item, count]) => (
              <div key={item} className="stat-row">
                <span>{item}:</span>
                <span className="stat-value">{count}</span>
              </div>
            ))}

            <h2 style={{ marginTop: 20 }}>Weapons</h2>
            {Object.keys(weapons).length === 0 && <div className="stat-row">No weapons</div>}
            {Object.entries(weapons).map(([name, w]) => (
              <div key={name} className="stat-row">
                <span>{name}</span>
                <div>
                  {equippedWeapon === name ? (
                    <span className="stat-value">Equipped</span>
                  ) : (
                    <button className="mini-btn" onClick={() => equipWeapon(name)}>Equip</button>
                  )}
                </div>
              </div>
            ))}

            <h2 style={{ marginTop: 20 }}>Spells</h2>
            {Object.keys(spells).length === 0 && <div className="stat-row">No spells</div>}
            {Object.entries(spells).map(([name, s]) => (
              <div key={name} className="stat-row">
                <span>{name}</span>
                <div>
                  {equippedSpell === name ? (
                    <span className="stat-value">Equipped</span>
                  ) : (
                    <button className="mini-btn" onClick={() => equipSpell(name)}>Equip</button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Stats;
