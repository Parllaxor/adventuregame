import React, { useState } from "react";
import "./App.css";
import ClassSelection from "./components/ClassSelection";
import GameScreen from "./components/GameScreen";
import Stats from "./components/Stats";

function App() {
  const [gameState, setGameState] = useState({
    is_game_started: false,
    chosen_class: null,
    current_biome: "Forest",
  });

  const [stats, setStats] = useState({
    HP: 20,
    max_HP: 20,
    Mana: 20,
    Energy: 100,
    Strength: 0,
    Defense: 0,
    Magic: 0,
    XP: 0,
    Level: 1,
  });

  const [inventory, setInventory] = useState({
    Wood: 0,
    Iron: 0,
    Gold: 5,
    Money: 5,
  });

  const [showStats, setShowStats] = useState(false);

  const handleClassSelect = async (classNum) => {
    try {
      const response = await fetch("http://localhost:5000/api/init", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chosen_class: classNum }),
      });
      const data = await response.json();
      setGameState(data.game_state);
      setStats(data.stats);
    } catch (error) {
      console.error("Error initializing game:", error);
    }
  };

  if (!gameState.is_game_started) {
    return <ClassSelection onSelectClass={handleClassSelect} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Adventure Game</h1>
        <div className="biome-display">Biome: {gameState.current_biome}</div>
      </header>

      {showStats ? (
        <Stats
          stats={stats}
          inventory={inventory}
          onBack={() => setShowStats(false)}
        />
      ) : (
        <GameScreen
          gameState={gameState}
          stats={stats}
          setStats={setStats}
          setGameState={setGameState}
          setInventory={setInventory}
          onShowStats={() => setShowStats(true)}
        />
      )}
    </div>
  );
}

export default App;
