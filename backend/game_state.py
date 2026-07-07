"""Shared game state and state helpers for the adventure game backend."""

from __future__ import annotations


# Shared in-memory game state used by the Flask routes and event handlers.
# Add new gameplay flags here when a feature needs to persist across requests.
game_state = {
    "player_name": "Hero",
    "chosen_class": None,
    "current_biome": "Forest",
    "is_game_started": False,
    "current_event_name": None,
    "in_combat": False,
    "current_enemy": None,
    "current_enemy_hp": 0,
    "current_enemy_max_hp": 0,
    "enemy_speed": 0,
    "minigame": None,
    "combat_session": {
        "turn_count": 0,
        "player_turn": True,
        "combat_log": [],
    },
    "time_healing": 0,
    "has_hypothermia": False,
    "blood_loss": 0,
    "is_bleeding": False,
    "is_sick": False,
    "recovering": 0,
}

character_stats = {
    "HP": 20,
    "max_HP": 20,
    "Mana": 20,
    "max_Mana": 20,
    "Energy": 100,
    "Strength": 0,
    "Defense": 0,
    "Magic": 0,
    "Dexterity": 0,
    "Speed": 0,
    "Swim": 0,
    "Intellect": 0,
    "XP": 0,
    "Level": 1,
    "Morale": 0,
}

previous_HP = character_stats["HP"]

inventory = {
    "Wood": 0,
    "Iron": 0,
    "Gold": 5,
    "Money": 5,
}

player_weapons = {}
equipped_weapon = "Fist"
player_spells = {}
equipped_spell = None
player_items = {}

# Reset helpers keep the game state consistent when a new run starts or a combat
# encounter ends. Extend these if a new subsystem needs to be cleared as well.
def reset_combat_session() -> None:
    """Reset combat turn tracking for a fresh encounter."""
    game_state["combat_session"] = {
        "turn_count": 0,
        "player_turn": True,
        "combat_log": [],
    }


def reset_game_state() -> None:
    """Reset to the default starting state for a new playthrough."""
    game_state.update(
        {
            "player_name": "Hero",
            "chosen_class": None,
            "current_biome": "Forest",
            "is_game_started": False,
            "current_event_name": None,
            "in_combat": False,
            "current_enemy": None,
            "current_enemy_hp": 0,
            "current_enemy_max_hp": 0,
            "enemy_speed": 0,
            "minigame": None,
            "time_healing": 0,
            "has_hypothermia": False,
            "blood_loss": 0,
            "is_bleeding": False,
            "is_sick": False,
            "recovering": 0,
        }
    )
    reset_combat_session()

    character_stats.update(
        {
            "HP": 20,
            "max_HP": 20,
            "Mana": 20,
            "max_Mana": 20,
            "Energy": 100,
            "Strength": 0,
            "Defense": 0,
            "Magic": 0,
            "Dexterity": 0,
            "Speed": 0,
            "Swim": 0,
            "Intellect": 0,
            "XP": 0,
            "Level": 1,
            "Morale": 0,
        }
    )

    inventory.clear()
    inventory.update({"Wood": 0, "Iron": 0, "Gold": 5, "Money": 5})

    player_weapons.clear()
    player_spells.clear()
    player_items.clear()

    global equipped_weapon, equipped_spell
    equipped_weapon = "Fist"
    equipped_spell = None


def get_state_snapshot() -> dict:
    """Return the current state in a JSON-friendly structure."""
    return {
        "game_state": game_state,
        "character_stats": character_stats,
        "inventory": inventory,
        "player_weapons": player_weapons,
        "player_spells": player_spells,
        "player_items": player_items,
        "equipped_weapon": equipped_weapon,
        "equipped_spell": equipped_spell,
    }
