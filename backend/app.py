from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import json
import os
import math
import requests

app = Flask(__name__, static_folder="", static_url_path="")
CORS(app)

# Proxy configuration for React dev server
REACT_DEV_SERVER = "http://localhost:3000"

# ==================== GAME STATE ====================
# This stores all player data. In production, you'd use a database.
game_state = {
    "player_name": "Hero",
    "chosen_class": None,  # 1=Warrior, 2=Mage, 3=Defender
    "current_biome": "Forest",
    "is_game_started": False,
    "current_event_name": None,
    "in_combat": False,
    "current_enemy": None,
    "current_enemy_hp": 0,

    # Status effects positive
    "time_healing": 0,

    # Status effects negative
    "has_hypothermia": False,
    "blood_lost": 0,
    "is_bleeding": False,
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
}

inventory = {
    "Wood": 0,
    "Iron": 0,
    "Gold": 5,
    "Money": 5,
}

# Weapons system
player_weapons = {}  # Will be populated based on class
equipped_weapon = "Fist"

# Spells system
player_spells = {}  # Will be populated based on class
equipped_spell = None

# Weapon definitions (simplified for web version)
WEAPONS_DB = {
    # ---------------- Legendary Weapons (20) ----------------

    "Reaper of the Gods": {"rarity": "Legendary", "damage": random.randint(80, 95), "hit_chance": 90, "type": "Melee", "drop_rate": 1, "special_power": "blind"},
    "Sun Blade": {"rarity": "Legendary", "damage": random.randint(50, 60), "hit_chance": 80, "type": "Melee", "drop_rate": 5, "special_power": "fire"},
    "Eternal Spear": {"rarity": "Legendary", "damage": random.randint(70, 85), "hit_chance": 85, "type": "Melee", "drop_rate": 3, "special_power": "shock"},
    "Dragon Fang": {"rarity": "Legendary", "damage": random.randint(85, 100), "hit_chance": 75, "type": "Melee", "drop_rate": 2, "special_power": "poison"},
    "Frostmourne": {"rarity": "Legendary", "damage": random.randint(80, 95), "hit_chance": 70, "type": "Melee", "drop_rate": 2, "special_power": "ice"},
    "Celestial Bow": {"rarity": "Legendary", "damage": random.randint(60, 80), "hit_chance": 95, "type": "Ranged", "drop_rate": 4, "special_power": "blind"},
    "Hammer of Titans": {"rarity": "Legendary", "damage": random.randint(90, 110), "hit_chance": 65, "type": "Melee", "drop_rate": 1, "special_power": "stun"},
    "Shadow Scythe": {"rarity": "Legendary", "damage": random.randint(75, 95), "hit_chance": 80, "type": "Melee", "drop_rate": 3, "special_power": "curse"},
    "Phoenix Staff": {"rarity": "Legendary", "damage": random.randint(55, 70), "hit_chance": 85, "type": "Magic", "drop_rate": 5, "special_power": "burn"},
    "Blade of Eternity": {"rarity": "Legendary", "damage": random.randint(95, 120), "hit_chance": 85, "type": "Melee", "drop_rate": 1, "special_power": "stun"},
    "Orb of Infinity": {"rarity": "Legendary", "damage": random.randint(70, 90), "hit_chance": 90, "type": "Magic", "drop_rate": 2, "special_power": "invisibility"},
    "Lance of Light": {"rarity": "Legendary", "damage": random.randint(75, 95), "hit_chance": 88, "type": "Melee", "drop_rate": 3, "special_power": "holy"},
    "Thunderstorm Bow": {"rarity": "Legendary", "damage": random.randint(80, 100), "hit_chance": 85, "type": "Ranged", "drop_rate": 2, "special_power": "shock"},
    "Crownbreaker Axe": {"rarity": "Legendary", "damage": random.randint(100, 120), "hit_chance": 70, "type": "Melee", "drop_rate": 1, "special_power": "none"},
    "Serpent Fang Dagger": {"rarity": "Legendary", "damage": random.randint(65, 80), "hit_chance": 95, "type": "Melee", "drop_rate": 4, "special_power": "poison"},
    "Volcanic Blade": {"rarity": "Legendary", "damage": random.randint(85, 105), "hit_chance": 80, "type": "Melee", "drop_rate": 3, "special_power": "fire"},
    "Scepter of Stars": {"rarity": "Legendary", "damage": random.randint(60, 75), "hit_chance": 90, "type": "Magic", "drop_rate": 4, "special_power": "meteor"},
    "Wraith Scythe": {"rarity": "Legendary", "damage": random.randint(90, 105), "hit_chance": 78, "type": "Melee", "drop_rate": 2, "special_power": "vampiric"},
    "Heaven’s Wrath": {"rarity": "Legendary", "damage": random.randint(100, 125), "hit_chance": 85, "type": "Melee", "drop_rate": 1, "special_power": "holy"},
    "Chrono Blade": {"rarity": "Legendary", "damage": random.randint(95, 110), "hit_chance": 82, "type": "Melee", "drop_rate": 2, "special_power": "time_warp"},

    # ---------------- Insane Weapons (20) ----------------

    "Nuclear Mace": {"rarity": "Insane", "damage": random.randint(80, 100), "hit_chance": 40, "type": "Melee", "drop_rate": 30, "special_power": "radiation"},
    "Blood Blade": {"rarity": "Insane", "damage": random.randint(30, 50), "hit_chance": 80, "type": "Melee", "drop_rate": 45, "special_power": "bleed"},
    "Chaos Axe": {"rarity": "Insane", "damage": random.randint(70, 90), "hit_chance": 50, "type": "Melee", "drop_rate": 25, "special_power": "confuse"},
    "Soul Breaker": {"rarity": "Insane", "damage": random.randint(65, 85), "hit_chance": 55, "type": "Melee", "drop_rate": 35, "special_power": "curse"},
    "Thunder Pike": {"rarity": "Insane", "damage": random.randint(60, 80), "hit_chance": 60, "type": "Melee", "drop_rate": 30, "special_power": "shock"},
    "Infernal Whip": {"rarity": "Insane", "damage": random.randint(50, 70), "hit_chance": 70, "type": "Melee", "drop_rate": 40, "special_power": "fire"},
    "Darkbow": {"rarity": "Insane", "damage": random.randint(45, 65), "hit_chance": 75, "type": "Ranged", "drop_rate": 30, "special_power": "drain"},
    "Plague Dagger": {"rarity": "Insane", "damage": random.randint(35, 50), "hit_chance": 85, "type": "Melee", "drop_rate": 50, "special_power": "poison"},
    "Venom Fang": {"rarity": "Insane", "damage": random.randint(40, 55), "hit_chance": 70, "type": "Melee", "drop_rate": 45, "special_power": "paralyze"},
    "Skull Crusher": {"rarity": "Insane", "damage": random.randint(80, 100), "hit_chance": 45, "type": "Melee", "drop_rate": 25, "special_power": "stun"},
    "Madman’s Blade": {"rarity": "Insane", "damage": random.randint(55, 75), "hit_chance": 65, "type": "Melee", "drop_rate": 35, "special_power": "berserk"},
    "Rage Spear": {"rarity": "Insane", "damage": random.randint(70, 90), "hit_chance": 60, "type": "Melee", "drop_rate": 30, "special_power": "frenzy"},
    "Night Terror": {"rarity": "Insane", "damage": random.randint(65, 85), "hit_chance": 55, "type": "Magic", "drop_rate": 40, "special_power": "fear"},
    "Acid Flail": {"rarity": "Insane", "damage": random.randint(60, 75), "hit_chance": 65, "type": "Melee", "drop_rate": 35, "special_power": "acid"},
    "Toxic Scythe": {"rarity": "Insane", "damage": random.randint(75, 95), "hit_chance": 55, "type": "Melee", "drop_rate": 30, "special_power": "toxin"},
    "Bloodfang Axe": {"rarity": "Insane", "damage": random.randint(70, 85), "hit_chance": 60, "type": "Melee", "drop_rate": 35, "special_power": "bleed"},
    "Corrupted Bow": {"rarity": "Insane", "damage": random.randint(50, 70), "hit_chance": 70, "type": "Ranged", "drop_rate": 40, "special_power": "curse"},
    "Soulfire Staff": {"rarity": "Insane", "damage": random.randint(45, 60), "hit_chance": 75, "type": "Magic", "drop_rate": 35, "special_power": "curse"},
    "Ruin Blade": {"rarity": "Insane", "damage": random.randint(85, 105), "hit_chance": 50, "type": "Melee", "drop_rate": 25, "special_power": "destruction"},
    "Howling Pike": {"rarity": "Insane", "damage": random.randint(60, 85), "hit_chance": 65, "type": "Melee", "drop_rate": 40, "special_power": "scream"},

# ---------------- Rare Weapons (20) ----------------

    "Bright Blade": {"rarity": "Rare", "damage": random.randint(20, 25), "hit_chance": 75, "type": "Melee", "drop_rate": 60, "special_power": "blind"},
    "Storm Bow": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 80, "type": "Ranged", "drop_rate": 50, "special_power": "shock"},
    "Crystal Dagger": {"rarity": "Rare", "damage": random.randint(22, 28), "hit_chance": 90, "type": "Melee", "drop_rate": 55, "special_power": "none"},
    "Shadow Katana": {"rarity": "Rare", "damage": random.randint(28, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "curse"},
    "Flame Mace": {"rarity": "Rare", "damage": random.randint(30, 45), "hit_chance": 65, "type": "Melee", "drop_rate": 50, "special_power": "fire"},
    "Moon Spear": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 70, "type": "Melee", "drop_rate": 55, "special_power": "freeze"},
    "Venom Crossbow": {"rarity": "Rare", "damage": random.randint(20, 30), "hit_chance": 80, "type": "Ranged", "drop_rate": 60, "special_power": "poison"},
    "Lava Sword": {"rarity": "Rare", "damage": random.randint(35, 45), "hit_chance": 60, "type": "Melee", "drop_rate": 40, "special_power": "fire"},
    "Frost Wand": {"rarity": "Rare", "damage": random.randint(18, 25), "hit_chance": 85, "type": "Magic", "drop_rate": 55, "special_power": "frost"},
    "Spirit Lance": {"rarity": "Rare", "damage": random.randint(30, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "drain"},
    "Runed Staff": {"rarity": "Rare", "damage": random.randint(20, 28), "hit_chance": 80, "type": "Magic", "drop_rate": 50, "special_power": "mana_boost"},
    "Glacier Hammer": {"rarity": "Rare", "damage": random.randint(32, 45), "hit_chance": 65, "type": "Melee", "drop_rate": 45, "special_power": "ice"},
    "Stormbreaker Axe": {"rarity": "Rare", "damage": random.randint(35, 50), "hit_chance": 70, "type": "Melee", "drop_rate": 40, "special_power": "shock"},
    "Venom Fang Sword": {"rarity": "Rare", "damage": random.randint(30, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "poison"},
    "Ashen Bow": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 80, "type": "Ranged", "drop_rate": 50, "special_power": "fire"},
    "Sunsteel Spear": {"rarity": "Rare", "damage": random.randint(28, 38), "hit_chance": 70, "type": "Melee", "drop_rate": 55, "special_power": "fire"},
    "Cursed Dagger": {"rarity": "Rare", "damage": random.randint(22, 32), "hit_chance": 85, "type": "Melee", "drop_rate": 60, "special_power": "curse"},
    "Echo Staff": {"rarity": "Rare", "damage": random.randint(18, 28), "hit_chance": 80, "type": "Magic", "drop_rate": 55, "special_power": "echo"},
    "Gale Blade": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 85, "type": "Melee", "drop_rate": 50, "special_power": "wind"},
    "Ember Pike": {"rarity": "Rare", "damage": random.randint(30, 42), "hit_chance": 70, "type": "Melee", "drop_rate": 45, "special_power": "fire"},

# ---------------- Uncommon Weapons (20) ----------------

    "Frozen Blade": {"rarity": "Uncommon", "damage": random.randint(17, 23), "hit_chance": 60, "type": "Melee", "drop_rate": 80, "special_power": "ice"},
    "Oak Bow": {"rarity": "Uncommon", "damage": random.randint(12, 20), "hit_chance": 70, "type": "Ranged", "drop_rate": 75, "special_power": "none"},
    "Stone Axe": {"rarity": "Uncommon", "damage": random.randint(15, 22), "hit_chance": 65, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Bronze Sword": {"rarity": "Uncommon", "damage": random.randint(14, 20), "hit_chance": 70, "type": "Melee", "drop_rate": 80, "special_power": "none"},
    "Steel Spear": {"rarity": "Uncommon", "damage": random.randint(18, 24), "hit_chance": 65, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Ashwood Staff": {"rarity": "Uncommon", "damage": random.randint(10, 18), "hit_chance": 75, "type": "Magic", "drop_rate": 80, "special_power": "none"},
    "Battle Pickaxe": {"rarity": "Uncommon", "damage": random.randint(16, 22), "hit_chance": 60, "type": "Melee", "drop_rate": 75, "special_power": "none"},
    "Crossbow": {"rarity": "Uncommon", "damage": random.randint(15, 20), "hit_chance": 70, "type": "Ranged", "drop_rate": 75, "special_power": "none"},
    "War Dagger": {"rarity": "Uncommon", "damage": random.randint(12, 18), "hit_chance": 85, "type": "Melee", "drop_rate": 85, "special_power": "none"},
    "Iron Mace": {"rarity": "Uncommon", "damage": random.randint(16, 22), "hit_chance": 60, "type": "Melee", "drop_rate": 80, "special_power": "none"},
    "Spiked Club": {"rarity": "Uncommon", "damage": random.randint(14, 20), "hit_chance": 65, "type": "Melee", "drop_rate": 75, "special_power": "none"},
    "Hunter’s Bow": {"rarity": "Uncommon", "damage": random.randint(12, 19), "hit_chance": 72, "type": "Ranged", "drop_rate": 75, "special_power": "none"},
    "Forged Spear": {"rarity": "Uncommon", "damage": random.randint(18, 25), "hit_chance": 68, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Steel Dagger": {"rarity": "Uncommon", "damage": random.randint(15, 20), "hit_chance": 80, "type": "Melee", "drop_rate": 80, "special_power": "none"},
    "Iron Pike": {"rarity": "Uncommon", "damage": random.randint(17, 23), "hit_chance": 65, "type": "Melee", "drop_rate": 75, "special_power": "none"},
    "Runed Mace": {"rarity": "Uncommon", "damage": random.randint(16, 21), "hit_chance": 70, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Reinforced Staff": {"rarity": "Uncommon", "damage": random.randint(10, 16), "hit_chance": 75, "type": "Magic", "drop_rate": 80, "special_power": "none"},
    "Wooden Bow": {"rarity": "Uncommon", "damage": random.randint(10, 15), "hit_chance": 70, "type": "Ranged", "drop_rate": 80, "special_power": "none"},
    "Chipped Axe": {"rarity": "Uncommon", "damage": random.randint(12, 18), "hit_chance": 65, "type": "Melee", "drop_rate": 85, "special_power": "none"},
    "Bronze Mace": {"rarity": "Uncommon", "damage": random.randint(13, 19), "hit_chance": 68, "type": "Melee", "drop_rate": 75, "special_power": "none"},

# ---------------- Common Weapons (20) ----------------

    "Iron Sword": {"rarity": "Common", "damage": random.randint(10, 20), "hit_chance": 60, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Sturdy Sword": {"rarity": "Common", "damage": random.randint(7, 15), "hit_chance": 70, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Rusty Sword": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 70, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Wooden Staff": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 70, "type": "Magic", "drop_rate": 100, "special_power": "none"},
    "Training Dagger": {"rarity": "Common", "damage": random.randint(3, 7), "hit_chance": 85, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Farmer’s Pitchfork": {"rarity": "Common", "damage": random.randint(5, 12), "hit_chance": 60, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Wooden Club": {"rarity": "Common", "damage": random.randint(6, 12), "hit_chance": 65, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Slingshot": {"rarity": "Common", "damage": random.randint(4, 9), "hit_chance": 75, "type": "Ranged", "drop_rate": 100, "special_power": "none"},
    "Practice Sword": {"rarity": "Common", "damage": random.randint(3, 8), "hit_chance": 80, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Stone Hammer": {"rarity": "Common", "damage": random.randint(6, 14), "hit_chance": 60, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Wooden Spear": {"rarity": "Common", "damage": random.randint(5, 12), "hit_chance": 65, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Copper Dagger": {"rarity": "Common", "damage": random.randint(4, 9), "hit_chance": 75, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Stone Club": {"rarity": "Common", "damage": random.randint(5, 11), "hit_chance": 65, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Basic Bow": {"rarity": "Common", "damage": random.randint(6, 12), "hit_chance": 70, "type": "Ranged", "drop_rate": 100, "special_power": "none"},
    "Iron Dagger": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 80, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Training Staff": {"rarity": "Common", "damage": random.randint(4, 8), "hit_chance": 75, "type": "Magic", "drop_rate": 95, "special_power": "none"},
    "Crude Spear": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 65, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Worn Sword": {"rarity": "Common", "damage": random.randint(6, 12), "hit_chance": 70, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Stone Spear": {"rarity": "Common", "damage": random.randint(5, 11), "hit_chance": 65, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Simple Club": {"rarity": "Common", "damage": random.randint(4, 9), "hit_chance": 70, "type": "Melee", "drop_rate": 100, "special_power": "none"},

    #---------------- Empty Weapon (1) ----------------

    "Fist": {"rarity": "None", "damage": 3, "hit_chance": 70, "type": "Melee", "drop_rate": 0, "special_power": "none"}
}

SPELLS_DB = {
    # Air / Wind
    "Wind Spell": {"type": "Air", "damage": random.randint(5, 8), "hit_chance": 95, "mana_cost": 1, "special_power": "none"},
    "Gust": {"type": "Air", "damage": random.randint(8, 15), "hit_chance": 70, "mana_cost": 2, "special_power": "none"},
    "Hurricane": {"type": "Air", "damage": random.randint(25, 35), "hit_chance": 50, "mana_cost": 8, "special_power": "stun"},
    "Whirlwind": {"type": "Air", "damage": random.randint(18, 28), "hit_chance": 65, "mana_cost": 5, "special_power": "none"},
    "Zephyr Slash": {"type": "Air", "damage": random.randint(12, 20), "hit_chance": 75, "mana_cost": 3, "special_power": "none"},

    # Ice
    "Ice Blast": {"type": "Ice", "damage": random.randint(10, 20), "hit_chance": 60, "mana_cost": 3, "special_power": "ice"},
    "Frost Spike": {"type": "Ice", "damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "ice"},
    "Glacier": {"type": "Ice", "damage": random.randint(30, 40), "hit_chance": 50, "mana_cost": 9, "special_power": "ice"},
    "Snowstorm": {"type": "Ice", "damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "blind"},
    "Frozen Shards": {"type": "Ice", "damage": random.randint(18, 24), "hit_chance": 70, "mana_cost": 5, "special_power": "bleed"},

    # Lightning
    "Lightning Bolt": {"type": "Lightning", "damage": random.randint(15, 20), "hit_chance": 75, "mana_cost": 3, "special_power": "stun"},
    "Thunder Strike": {"type": "Lightning", "damage": random.randint(20, 30), "hit_chance": 65, "mana_cost": 5, "special_power": "stun"},
    "Charge Blast": {"type": "Lightning", "damage": random.randint(15, 25), "hit_chance": 70, "mana_cost": 6, "special_power": "stun"},
    "Storm Surge": {"type": "Lightning", "damage": random.randint(25, 35), "hit_chance": 55, "mana_cost": 7, "special_power": "stun"},
    "Ball Lightning": {"type": "Lightning", "damage": random.randint(18, 26), "hit_chance": 65, "mana_cost": 5, "special_power": "fire"},

    # Fire
    "Fireball": {"type": "Fire", "damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "fire"},
    "Flame Wave": {"type": "Fire", "damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 5, "special_power": "fire"},
    "Inferno": {"type": "Fire", "damage": random.randint(35, 50), "hit_chance": 50, "mana_cost": 10, "special_power": "fire"},
    "Ember Shot": {"type": "Fire", "damage": random.randint(8, 15), "hit_chance": 80, "mana_cost": 2, "special_power": "fire"},
    "Dragon’s Breath": {"type": "Fire", "damage": random.randint(25, 40), "hit_chance": 55, "mana_cost": 7, "special_power": "fire"},

    # Water
    "Water Jet": {"type": "Water", "damage": random.randint(12, 20), "hit_chance": 70, "mana_cost": 3, "special_power": "none"},
    "Tidal Wave": {"type": "Water", "damage": random.randint(28, 38), "hit_chance": 55, "mana_cost": 8, "special_power": "stun"},
    "Bubble Prison": {"type": "Water", "damage": random.randint(8, 12), "hit_chance": 85, "mana_cost": 4, "special_power": "none"},
    "Aqua Slash": {"type": "Water", "damage": random.randint(15, 22), "hit_chance": 75, "mana_cost": 3, "special_power": "bleed"},
    "Rainstorm": {"type": "Water", "damage": random.randint(18, 25), "hit_chance": 70, "mana_cost": 5, "special_power": "none"},

    # Earth
    "Rock Throw": {"type": "Earth", "damage": random.randint(10, 18), "hit_chance": 70, "mana_cost": 3, "special_power": "none"},
    "Earthquake": {"type": "Earth", "damage": random.randint(30, 45), "hit_chance": 50, "mana_cost": 9, "special_power": "stun"},
    "Stone Spike": {"type": "Earth", "damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "none"},
    "Sandstorm": {"type": "Earth", "damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "blind"},
    "Iron Fist": {"type": "Earth", "damage": random.randint(18, 26), "hit_chance": 70, "mana_cost": 5, "special_power": "broken_armor"},

    # Dark
    "Shadow Bolt": {"type": "Dark", "damage": random.randint(15, 25), "hit_chance": 70, "mana_cost": 4, "special_power": "curse"},
    "Nightmare": {"type": "Dark", "damage": random.randint(25, 35), "hit_chance": 55, "mana_cost": 7, "special_power": "curse"},
    "Soul Drain": {"type": "Dark", "damage": random.randint(12, 20), "hit_chance": 65, "mana_cost": 5, "special_power": "vampiric"},
    "Dark Wave": {"type": "Dark", "damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "curse"},
    "Abyssal Flame": {"type": "Dark", "damage": random.randint(30, 40), "hit_chance": 50, "mana_cost": 8, "special_power": "burn"},

    # Holy / Light
    "Holy Beam": {"type": "Light", "damage": random.randint(15, 25), "hit_chance": 75, "mana_cost": 4, "special_power": "heal"},
    "Radiant Slash": {"type": "Light", "damage": random.randint(20, 30), "hit_chance": 70, "mana_cost": 5, "special_power": "blind"},
    "Healing Light": {"type": "Light", "damage": 0, "hit_chance": 100, "mana_cost": 6, "special_power": "heal"},
    "Smite": {"type": "Light", "damage": random.randint(25, 35), "hit_chance": 65, "mana_cost": 7, "special_power": "burn"},
    "Sunburst": {"type": "Light", "damage": random.randint(30, 40), "hit_chance": 55, "mana_cost": 9, "special_power": "burn"},

    # Arcane / Utility
    "Arcane Missile": {"type": "Arcane", "damage": random.randint(12, 20), "hit_chance": 80, "mana_cost": 3, "special_power": "none"},
    "Mana Burn": {"type": "Arcane", "damage": random.randint(10, 15), "hit_chance": 70, "mana_cost": 4, "special_power": "mana_drain"},
    "Time Stop": {"type": "Arcane", "damage": 0, "hit_chance": 100, "mana_cost": 12, "special_power": "stun"},
    "Teleport Strike": {"type": "Arcane", "damage": random.randint(20, 28), "hit_chance": 85, "mana_cost": 6, "special_power": "teleport"},
    "Mirror Image": {"type": "Arcane", "damage": 0, "hit_chance": 100, "mana_cost": 5, "special_power": "confusion"},
}

# Enemy definitions - base stats without scaling
ENEMIES_DB = {
    "Goblin": {"hp": [15, 25], "damage": [3, 8], "xp_reward": 20, "money_reward": [5, 15], "level_scaling": 0.4, "status_effect": None},
    "Orc": {"hp": [30, 50], "damage": [8, 15], "xp_reward": 50, "money_reward": [20, 40], "level_scaling": 0.8, "status_effect": None},
    "Dragon": {"hp": [100, 150], "damage": [20, 40], "xp_reward": 200, "money_reward": [100, 200], "level_scaling": 1.5, "status_effect": None},
    "Pirate": {"hp": [20, 35], "damage": [5, 12], "xp_reward": 30, "money_reward": [15, 30], "level_scaling": 0.5, "status_effect": None},
    "Siren": {"hp": [50, 80], "damage": [15, 22], "xp_reward": 100, "money_reward": [35, 55], "level_scaling": 1.0, "status_effect": None},
    "Ice Golem": {"hp": [60, 90], "damage": [12, 18], "xp_reward": 60, "money_reward": [30, 50], "level_scaling": 1.0, "status_effect": None},
    "Troll": {"hp": [40, 70], "damage": [10, 20], "xp_reward": 50, "money_reward": [25, 45], "level_scaling": 0.9, "status_effect": None},
    "Skeleton": {"hp": [25, 45], "damage": [5, 10], "xp_reward": 30, "money_reward": [10, 20], "level_scaling": 0.6, "status_effect": None},
    "Spider": {"hp": [10, 20], "damage": [3, 6], "xp_reward": 15, "money_reward": [5, 10], "level_scaling": 0.3, "status_effect": None},
}

def scale_enemy_stats(enemy_type, player_level):
    """Scale enemy stats based on player level for balanced combat"""
    if enemy_type not in ENEMIES_DB:
        return None
    
    base_enemy = ENEMIES_DB[enemy_type].copy()
    scaling_factor = base_enemy.pop("level_scaling")
    
    # Scale HP: increases with level
    hp_min, hp_max = base_enemy["hp"]
    level_bonus = player_level * scaling_factor
    base_enemy["hp"] = [
        int(hp_min + level_bonus),
        int(hp_max + level_bonus)
    ]
    
    # Scale damage: increases with level
    dmg_min, dmg_max = base_enemy["damage"]
    base_enemy["damage"] = [
        int(dmg_min + level_bonus * 0.6),
        int(dmg_max + level_bonus * 0.6)
    ]
    
    # Scale XP reward: increases with level
    base_enemy["xp_reward"] = int(base_enemy["xp_reward"] + (player_level - 1) * 10)
    
    # Scale money reward: increases with level
    money_min, money_max = base_enemy["money_reward"]
    base_enemy["money_reward"] = [
        int(money_min + level_bonus * 0.5),
        int(money_max + level_bonus * 0.5)
    ]
    
    return base_enemy

def start_battle(enemy_type):
    """
    Trigger a battle with any enemy type from event choices.
    Scales enemy stats based on player level and sets up combat state.
    
    Usage from event choice handlers:
        return start_battle("Orc")  # Returns proper battle response
    
    Returns a dict with battle_started flag and scaled enemy stats
    """
    if enemy_type not in ENEMIES_DB:
        return {"text": f"Enemy {enemy_type} not found", "continue": True}
    
    game_state["in_combat"] = True
    scaled_enemy = scale_enemy_stats(enemy_type, character_stats["Level"])
    enemy_hp = random.randint(scaled_enemy["hp"][0], scaled_enemy["hp"][1])
    
    game_state["current_enemy"] = enemy_type
    game_state["current_enemy_hp"] = enemy_hp
    game_state["current_enemy_max_hp"] = enemy_hp
    
    return {
        "text": f"⚔️ COMBAT INITIATED! ⚔️\n\nA {enemy_type} appears and prepares to attack!",
        "battle_started": True,
        "enemy": enemy_type,
        "enemy_hp": enemy_hp,
        "enemy_max_hp": enemy_hp,
        "continue": False
    }

def start_battle_with_intro(enemy_type, narrative):
    """
    Show a narrative intro screen before triggering battle.
    Stores the enemy type in game_state and returns the narrative as an event.
    When player clicks "Fight!", the battle will start.
    
    Usage from event choice handlers:
        return start_battle_with_intro("Orc", "You were ambushed by an orc!")
    
    The "Fight!" button will automatically trigger start_battle(enemy_type)
    """
    if enemy_type not in ENEMIES_DB:
        return {"text": f"Enemy {enemy_type} not found", "continue": True}
    
    # Store pending battle info
    game_state["pending_battle_enemy"] = enemy_type
    
    return {
        "text": narrative,
        "choices": ["Fight!"],
        "battle_intro": True,
        "continue": False
    }

# ==================== ROUTES FOR STATIC FILES ====================

@app.route("/")
def root():
    """Serve the main index.html"""
    return send_from_directory("../", "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static files"""
    return send_from_directory("../", filename)

# ==================== EVENTS ====================
# Event functions return (text, choices)

def trigger_swamp_event():
    """Swamp - Scavenge for resources or explore"""
    text = "Another challenge awaits! You find yourself in a thick swamp. What will you do?\n\n1. Scavenge for resources\n2. Explore further\n3. Rest yourself"
    choices = ["Scavenge", "Explore", "Rest"]
    return text, choices

def trigger_gnome_ambush():
    """Forest - Ambushed by gnomes"""
    text = "While stumbling across the forest, you are ambushed by a group of gnomes. What will you do?\n\n1. Spin attack with sword\n2. Cast lightning strike\n3. Attempt to bribe them"
    choices = ["Spin Attack", "Lightning Strike", "Bribe"]
    return text, choices

def trigger_igloo_event():
    """Tundra - Find an igloo in the snow"""
    text = "You come across an igloo in the snow-covered landscape. What do you do?\n\n1. Take a nap\n2. Melt it to search for goods\n3. Take spell book"
    choices = ["Nap", "Melt Igloo", "Take Spell Book"]
    return text, choices

def trigger_cave_event():
    """Mountain - Explore a cave"""
    text = "You discover a dark cave. What do you do?\n\n1. Venture inside\n2. Set up camp outside\n3. Leave immediately"
    choices = ["Venture In", "Camp Outside", "Leave"]
    return text, choices

def trigger_cave_2():
    """New Event: Deeper cave exploration with rare loot"""
    text = "You venture deeper into the cave and discover a hidden chamber filled with treasure! Among the loot, you find a rare weapon.\n\n1. Take the weapon\n2. Search for more treasure\n3. Leave the cave"
    choices = ["Take Weapon", "Search More", "Leave"]
    return text, choices

def trigger_cave_3():
    """New Event: Cave with a sleeping monster"""
    text = "As you explore the cave, you accidentally wake a sleeping monster! It looks angry. What do you do?\n\n1. Fight the monster\n2. Try to sneak past it\n3. Flee the cave"
    choices = ["Fight", "Sneak", "Flee"]
    return text, choices

def trigger_cave_4():
    """New Event: Cave with a mysterious puzzle"""
    text = "You find a mysterious puzzle blocking your path deeper into the cave. It looks ancient and complex. What do you do?\n\n1. Attempt to solve the puzzle\n2. Look for clues around the cave\n3. Ignore it and continue exploring"
    choices = ["Solve Puzzle", "Look for Clues", "Ignore"]
    return text, choices

def trigger_river_event():
    """Plains - Encounter a river"""
    text = "You come upon a rushing river. How do you cross?\n\n1. Swim across\n2. Build a raft\n3. Look for a bridge"
    choices = ["Swim", "Build Raft", "Find Bridge"]
    return text, choices

def trigger_shipwreck_event():
    """Ocean - Find a shipwreck"""
    text = "You discover an abandoned shipwreck. What do you do?\n\n1. Explore for treasure\n2. Search for survivors\n3. Avoid it and sail on"
    choices = ["Explore", "Search", "Avoid"]
    return text, choices

def trigger_desert_oasis():
    """Desert - Find an oasis"""
    text = "The desert heat is overwhelming. Suddenly, you see an oasis! What do you do?\n\n1. Drink the water\n2. Set up camp\n3. Continue searching for civilization"
    choices = ["Drink", "Camp", "Continue"]
    return text, choices

def trigger_jungle_vines():
    """Jungle - Blocked by vines"""
    text = "Thick vines block your path in the jungle. What do you do?\n\n1. Cut through them\n2. Climb over them\n3. Go around them"
    choices = ["Cut", "Climb", "Around"]
    return text, choices

def trigger_old_ruins():
    """Forest - Discover ancient ruins"""
    text = "You stumble upon ancient ruins hidden in the forest. What do you do?\n\n1. Enter and explore\n2. Search the perimeter\n3. Leave immediately"
    choices = ["Enter", "Search", "Leave"]
    return text, choices

def trigger_merchant_caravan():
    """Plains - Meet a merchant caravan"""
    text = "You encounter a merchant caravan on the road. What do you do?\n\n1. Trade with them\n2. Ask for directions\n3. Rob them"
    choices = ["Trade", "Ask Directions", "Rob"]
    return text, choices

def trigger_pirate_attack():
    if game_state["chosen_class"] in [1, 3]:  # Warrior or Defender
        text = "You engage in combat with the pirates!\n\n1. Board the pirate boat\n2. Fire a cannon at them\n3. Jump into the water"
        choices = ["Board Boat", "Fire Cannon", "Jump in Water"]
    else:  # Mage
        text = "You engage in combat with the pirates!\n\n1. Board their boat\n2. Conjure a magical storm\n3. Jump into the water"
        choices = ["Board Boat", "Conjure Storm", "Jump in Water"]
    return text, choices

def trigger_forest_encounter():
    text = "You stumble upon a group of gnomes in the forest.\n\n1. Attack them\n2. Try to talk to them\n3. Run away"
    choices = ["Attack", "Talk", "Run"]
    return text, choices

def trigger_arrow_to_the_knee():
    text = "While adventuring, you take by an arrow in the knee. Ouch! What do you do?\n\n1. Keep going despite the pain\n2. Rest and tend to the wound\n3. Seek out a healer"
    choices = ["Keep Going", "Rest", "Seek Healer"]
    return text, choices

def trigger_rest():
    text = "You rest under a tree and recover your strength."
    choices = ["Continue"]
    return text, choices

def trigger_goblin_fight():
    text = "A goblin appears! What do you do?\n\n1. Fight with sword\n2. Cast a spell\n3. Try to flee"
    choices = ["Fight", "Cast Spell", "Flee"]
    return text, choices

def trigger_ancient_tomb():
    """New Event: Discover an ancient tomb with weapon"""
    text = "You discover an ancient tomb hidden beneath moss and vines. Inside, you see a glowing weapon on a stone pedestal.\n\n1. Take the weapon\n2. Search for treasure first\n3. Leave it alone"
    choices = ["Take Weapon", "Search Treasure", "Leave"]
    return text, choices

def trigger_blacksmith_forge():
    """New Event: Find an abandoned blacksmith with rare weapon"""
    text = "You stumble upon an abandoned blacksmith's forge. The fire still burns! A masterwork weapon hangs on the wall.\n\n1. Take the weapon\n2. Talk to the unseen blacksmith\n3. Leave"
    choices = ["Take Weapon", "Talk", "Leave"]
    return text, choices

def trigger_dragon_nest():
    """New Event: Encounter a dragon's nest"""
    text = "You find a dragon's nest! Gold gleams everywhere, but there's also a dragon egg.\n\n1. Grab the gold\n2. Take the dragon egg\n3. Flee before the dragon returns"
    choices = ["Grab Gold", "Take Egg", "Flee"]
    return text, choices

def trigger_cursed_library():
    """New Event: Ancient library with cursed items"""
    text = "An eerie library glows with magical energy. Ancient tomes line the shelves, and a mysterious artifact floats in the center.\n\n1. Touch the artifact\n2. Read the books\n3. Run away"
    choices = ["Touch Artifact", "Read Books", "Run"]
    return text, choices

def trigger_lost_temple():
    """New Event: Temple with treasure and dangers"""
    text = "You enter a lost temple covered in gold and jewels. Pressure plates cover the floor!\n\n1. Carefully walk to the center\n2. Smash your way through\n3. Mark the exit and leave"
    choices = ["Walk Carefully", "Smash Through", "Mark Exit"]
    return text, choices

def trigger_crystal_cave():
    """New Event: Cave of crystalline structures"""
    text = "A beautiful cave of blue crystals surrounds you. Some crystals glow with strange power.\n\n1. Harvest the crystals\n2. Meditate among them\n3. Leave"
    choices = ["Harvest", "Meditate", "Leave"]
    return text, choices

def trigger_phoenix_shrine():
    """New Event: Shrine dedicated to mythical phoenix"""
    text = "A sacred shrine glows with an eternal flame. A phoenix suddenly appears from the fire!\n\n1. Show respect\n2. Grab what you can\n3. Run in fear"
    choices = ["Show Respect", "Grab", "Run"]
    return text, choices

def trigger_goblin_settlement():
    """New Event: Find a goblin village"""
    text = "You discover a goblin settlement. They're busy trading and crafting weapons.\n\n1. Sneak in and steal\n2. Trade with them\n3. Attack them"
    choices = ["Sneak", "Trade", "Attack"]
    return text, choices

def trigger_wizard_tower():
    """New Event: Magical tower in the sky"""
    text = "A floating tower materializes before you! A wizard waves from the top.\n\n1. Climb the tower\n2. Use magic to ascend\n3. Ignore it"
    choices = ["Climb", "Magic", "Ignore"]
    return text, choices

def trigger_sunken_ruin():
    """New Event: Underwater ruins"""
    text = "You find sunken ruins in a flooded cavern. Valuables glimmer below.\n\n1. Dive down\n2. Call for help\n3. Mark it on map"
    choices = ["Dive", "Call Help", "Mark Map"]
    return text, choices

def trigger_dark_forest():
    """New Event: Dark cursed forest"""
    text = "The forest grows darker. Strange glowing eyes watch you from the trees.\n\n1. Investigate the eyes\n2. Light a fire\n3. Leave quickly"
    choices = ["Investigate", "Light Fire", "Leave"]
    return text, choices

def trigger_ice_fishing():
    """"New Event: Ice fishing on a frozen lake"""
    text = "You find a frozen lake with holes cut into the ice. A fishing rod lies nearby.\n\n1. Swim\n2. Fish\n3. Enjoy View"
    choices = ["Swim", "Fish", "Enjoy View"]
    return text, choices

def trigger_ancient_grove():
    """New Event: Enchanted grove with mystical properties"""
    text = "You enter an ancient grove where the trees whisper secrets. A magical aura fills the air.\n\n1. Listen to the trees\n2. Gather herbs\n3. Rest in the grove"
    choices = ["Listen", "Gather", "Rest"]
    return text, choices

def trigger_woman_encounter():
    """New Event: The beautiful singing woman"""
    text = "You hear a distant melody, seeming to emanate from the waves. You see a beautiful woman on the shore, and head towards her. \n\n1. Approach her\n2. Prepare to strike\n3. Ignore her and continue on your way"
    choices = ["Approach", "Strike", "Ignore"]
    return text, choices

def trigger_orc_battle():
    """Forest - Encounter a charging Orc! Battle trigger event"""
    text = "CRASH! A massive Orc bursts through the trees!\n\nThe beast, covered in scars and wielding a crude club, roars at you. There's no escape—combat is inevitable!\n\nReady yourself for battle!"
    choices = ["Draw Weapon", "Cast Spell", "Defend"]
    return text, choices

def trigger_biome_transition():
    """New Event: Transition to a new biome"""
    text = f"You wander far and wide, until you discover a new biome. Will you continue exploring the {game_state['current_biome']}, or move on?\n\n1. Stay in the {game_state['current_biome']}\n2. Move to a new biome"
    choices = ["Stay", "Leave"]
    return text, choices

# Event pool by biome
EVENTS = {
    "Forest": [trigger_biome_transition, trigger_gnome_ambush, trigger_old_ruins, trigger_forest_encounter, trigger_ancient_tomb, trigger_crystal_cave, trigger_dark_forest, trigger_orc_battle],
    "Ocean": [trigger_biome_transition, trigger_pirate_attack, trigger_shipwreck_event, trigger_sunken_ruin, trigger_woman_encounter],
    "Plains": [trigger_arrow_to_the_knee, trigger_biome_transition, trigger_river_event, trigger_merchant_caravan, trigger_goblin_fight, trigger_goblin_settlement],
    "Swamp": [trigger_biome_transition, trigger_swamp_event, trigger_cursed_library, trigger_ancient_grove],
    "Tundra": [trigger_biome_transition, trigger_igloo_event, trigger_lost_temple],
    "Mountain": [trigger_biome_transition, trigger_cave_event, trigger_blacksmith_forge, trigger_wizard_tower],
    "Desert": [trigger_biome_transition, trigger_desert_oasis, trigger_dragon_nest],
    "Jungle": [trigger_biome_transition, trigger_jungle_vines, trigger_phoenix_shrine],
}

# List of available biomes (derived from EVENTS keys)
BIOMES = list(EVENTS.keys())

# ==================== WEAPON SYSTEM FUNCTIONS ====================

def weapon_get(weapon_name):
    """Add a weapon to player inventory"""
    global player_weapons
    if weapon_name in WEAPONS_DB and weapon_name not in player_weapons:
        player_weapons[weapon_name] = WEAPONS_DB[weapon_name]
        return f"Obtained: {weapon_name}!"
    elif weapon_name in player_weapons:
        return f"You already have {weapon_name}!"
    else:
        return "Weapon not found in database"

def spell_get(spell_name):
    """Add a spell to player inventory"""
    global player_spells
    if spell_name in SPELLS_DB and spell_name not in player_spells:
        player_spells[spell_name] = SPELLS_DB[spell_name]
        return f"Obtained: {spell_name}!"
    elif spell_name in player_spells:
        return f"You already have {spell_name}!"
    else:
        return "Spell not found in database"

def get_random_weapon_by_rarity(rarity):
    """
    Get a random weapon of a specific rarity level.
    Valid rarities: "Legendary", "Rare", "Uncommon", "Common"
    """
    weapons_of_rarity = [
        weapon_name for weapon_name, stats in WEAPONS_DB.items()
        if stats.get("rarity") == rarity
    ]
    
    if not weapons_of_rarity:
        return None
    
    return random.choice(weapons_of_rarity)


def get_random_spell_of_type(spell_type):
    """
    Get a random spell of a specific arcane type.
    Valid types: "Air", "Ice", "Lightning", "Fire", "Water", "Earth", "Dark", "Holy", "Arcane"
    """
    spells_of_type = [
        spell_name for spell_name, stats in SPELLS_DB.items()
        if stats.get("type") == spell_type
    ]
    
    if not spells_of_type:
        return None
    
    return random.choice(spells_of_type)

def get_equipped_weapon_data():
    """
    Get the full weapon data for the currently equipped weapon.
    Returns the weapon dict from WEAPONS_DB.
    """
    global equipped_weapon
    
    if equipped_weapon and equipped_weapon in WEAPONS_DB:
        return WEAPONS_DB[equipped_weapon]
    else:
        # Fallback to Fist if nothing equipped
        return WEAPONS_DB.get("Fist", {"damage": [0, 0]})

def calculate_weapon_damage(use_max=True):
    """
    Calculate total weapon damage with stat modifiers.
    
    Args:
        use_max (bool): If True, uses max damage roll. If False, uses min damage.
    
    Returns:
        int: Total damage including weapon base + strength/dexterity modifiers
    """
    weapon = get_equipped_weapon_data()
    damage_range = weapon.get("damage", [0, 0])
    
    # Choose min or max damage
    base_damage = damage_range[1] if use_max else damage_range[0]
    
    # Add strength modifier (same formula as combat)
    strength_bonus = math.floor(character_stats.get("Strength", 0) * 0.6)
    
    # Add dexterity modifier
    dex_bonus = math.floor(character_stats.get("Dexterity", 0) * 0.3)
    
    total_damage = max(0, base_damage + strength_bonus + dex_bonus)
    return total_damage

def get_total_player_power():
    """
    Get an overall power level combining weapon and strength.
    Useful for comparing against enemy difficulty thresholds.
    
    Returns:
        int: Total power score
    """
    return character_stats.get("Strength", 0) + calculate_weapon_damage()

def get_equipped_spell_data():
    """
    Get the full spell data for the currently equipped spell.
    Returns the spell dict from SPELLS_DB.
    """
    global equipped_spell
    
    if equipped_spell and equipped_spell in SPELLS_DB:
        return SPELLS_DB[equipped_spell]
    else:
        # Fallback to empty spell if none equipped
        return {"damage": [0, 0], "mana_cost": 0}

def calculate_spell_damage(use_max=True):
    """
    Calculate total spell damage with stat modifiers.
    
    Args:
        use_max (bool): If True, uses max damage roll. If False, uses min damage.
    
    Returns:
        int: Total damage including spell base + magic/intellect modifiers
    """
    spell = get_equipped_spell_data()
    damage_range = spell.get("damage", [0, 0])
    
    # Choose min or max damage
    base_damage = damage_range[1] if use_max else damage_range[0]
    
    # Add magic modifier (same formula as combat)
    magic_bonus = math.floor(character_stats.get("Magic", 0) * 0.7)
    
    # Add intellect modifier
    intellect_bonus = math.floor(character_stats.get("Intellect", 0) * 0.4)
    
    total_damage = max(0, base_damage + magic_bonus + intellect_bonus)
    return total_damage

def get_total_spell_power():
    """
    Get an overall spell power level combining magic and spell damage.
    Useful for comparing against magical difficulty thresholds.
    
    Returns:
        int: Total spell power score
    """
    return character_stats.get("Magic", 0) + calculate_spell_damage()

def teleport_random_biome():
    """Teleport the player to a random different biome."""
    available = [b for b in BIOMES if b != game_state.get("current_biome")]
    if not available:
        available = BIOMES
    new_biome = random.choice(available)
    while new_biome == game_state["current_biome"]: # Don't stay in the same biome
        new_biome = random.choice(available)
    game_state["current_biome"] = new_biome
    return new_biome


def teleport_to_biome(biome_name):
    """Teleport the player to a specific biome if valid."""
    if biome_name not in BIOMES:
        raise ValueError("Invalid biome")
    game_state["current_biome"] = biome_name
    return biome_name

# ==================== ROUTES ====================

@app.route("/api/init", methods=["POST"])
def init_game():
    """Initialize a new game with character class selection"""
    global equipped_weapon, equipped_spell, player_weapons, player_spells
    
    data = request.json
    chosen_class = data.get("chosen_class")  # 1, 2, or 3
    
    game_state["chosen_class"] = chosen_class
    game_state["is_game_started"] = True
    # Start in Forest by default, but small chance to start in another biome
    game_state["current_biome"] = "Forest"
    try:
        if random.random() < 0.10:  # 10% chance to start in a random biome
            other = [b for b in BIOMES if b != "Forest"]
            if other:
                game_state["current_biome"] = random.choice(other)
    except Exception:
        # BIOMES may not be defined in some initialization orders; fall back to Forest
        game_state["current_biome"] = "Forest"
    
    # Apply class bonuses and starting weapons
    if chosen_class == 1:  # Warrior
        character_stats["Strength"] += 5
        character_stats["Defense"] += 3
        character_stats["HP"] = 40
        character_stats["max_HP"] = 40
        player_weapons = {"Iron Sword": WEAPONS_DB["Iron Sword"], "Bronze Sword": WEAPONS_DB["Bronze Sword"]}
        equipped_weapon = "Iron Sword"
    elif chosen_class == 2:  # Mage
        character_stats["Magic"] += 5
        character_stats["Mana"] = 50
        character_stats["max_Mana"] = 50
        player_spells = {"Wind Spell": SPELLS_DB["Wind Spell"], "Lightning Bolt": SPELLS_DB["Lightning Bolt"], "Fireball": SPELLS_DB["Fireball"]}
        equipped_spell = "Lightning Bolt"
        equipped_weapon = "Wooden Club"
        player_weapons = {"Wooden Club": WEAPONS_DB["Wooden Club"]}
    elif chosen_class == 3:  # Defender
        character_stats["Defense"] += 5
        character_stats["Strength"] += 3
        character_stats["HP"] = 50
        character_stats["max_HP"] = 50
        player_weapons = {"Iron Mace": WEAPONS_DB["Iron Mace"], "Bronze Sword": WEAPONS_DB["Bronze Sword"]}
        equipped_weapon = "Iron Mace"

    # Apply small random bonus to all stats for extra variety
    total_additional_stats = 10  # Total points to distribute randomly
    additional_stats = 0

    # Prioritize certain additional (not already increased) stats on startup based on class, but still add some randomness. The later in the list, the lower priority for random bonuses.
    mage_stat_priorities = ["Intellect", "Dexterity", "HP", "Swim", "Defense", "Strength"]
    defender_stat_priority = ["Strength", "Magic", "Intellect", "Dexterity", "Mana", "Swim"]
    warrior_stat_priority = ["HP", "Swim", "Dexterity", "Intellect", "Magic", "Mana"]

    if game_state["chosen_class"] == 1:
        stat_priorities = warrior_stat_priority
    elif game_state["chosen_class"] == 2:
        stat_priorities = mage_stat_priorities
    elif game_state["chosen_class"] == 3:
        stat_priorities = defender_stat_priority

    while additional_stats <= total_additional_stats:
        for stat in stat_priorities:
            if additional_stats > total_additional_stats: # Exit for loop if we've already added enough stats
                break
            added_amount = random.randint(0, 2)
            if added_amount + additional_stats > total_additional_stats:
                added_amount = total_additional_stats - additional_stats  # Don't exceed total
            character_stats[stat] += added_amount  # Randomly add 0, 1, or 2 to each stat. The later in the list, the lower priority
            additional_stats += added_amount

    previous_HP = character_stats["HP"]  # Set previous HP for regen calculations at game start
    
    return jsonify({
        "message": f"Game started! You are a class {chosen_class}",
        "game_state": game_state,
        "stats": character_stats,
        "weapons": player_weapons,
        "spells": player_spells,
        "equipped_weapon": equipped_weapon,
        "equipped_spell": equipped_spell,
    })

@app.route("/api/event", methods=["GET"])
def get_event():
    """Trigger a random event based on current biome"""
    biome = game_state.get("current_biome", "Forest")
    
    # Get random event for this biome
    available_events = EVENTS.get(biome, EVENTS["Forest"])
    selected_event = random.choice(available_events)
    if game_state.get("current_event_name") == selected_event.__name__:
        # Avoid repeating the same event twice in a row
        available_events = [e for e in available_events if e.__name__ != game_state["current_event_name"]]
        if available_events:
            selected_event = random.choice(available_events)
    
    text, choices = selected_event()
    event_name = selected_event.__name__
    
    game_state["current_event_name"] = event_name
    
    return jsonify({
        "event_name": event_name,
        "text": text,
        "choices": choices,
    })


@app.route("/api/teleport-random", methods=["POST"])
def api_teleport_random():
    """Endpoint to teleport player to a random biome."""
    try:
        new_biome = teleport_random_biome()
        return jsonify({"new_biome": new_biome, "game_state": game_state})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/teleport-to", methods=["POST"])
def api_teleport_to():
    """Endpoint to teleport player to a specific biome. Provide JSON {"biome": "Desert"}."""
    data = request.json or {}
    biome = data.get("biome")
    if not biome:
        return jsonify({"error": "No biome provided", "available": BIOMES}), 400
    if biome not in BIOMES:
        return jsonify({"error": "Biome not found", "available": BIOMES}), 400
    try:
        teleport_to_biome(biome)
        return jsonify({"new_biome": biome, "game_state": game_state})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/choose", methods=["POST"])
def handle_choice():
    """Handle player's choice in an event"""
    data = request.json
    choice = data.get("choice")
    event_name = data.get("event_name")
    
    # Determine outcome based on event and choice
    outcome = process_choice(event_name, choice)

    # Passive outcomes that tick once after every choice
    
    heal_player()
    check_passive_effects()
    check_game_state()
    
    # Check for level up
    level_up_result = level_up()
    
    # If level up occurred, merge the level up data into outcome
    if level_up_result.get("is_level_up", False):
        outcome["is_level_up"] = True
        outcome["new_level"] = level_up_result["new_level"]
        outcome["stat_increases"] = level_up_result["stat_increases"]
        outcome["new_stats"] = level_up_result["new_stats"]
        outcome["level_up_text"] = level_up_result["text"]
    
    return jsonify(outcome)

def heal_player():
    """Heal the player if an event calls for it"""
    
    game_state["has_hypothermia"] = False
    game_state["is_bleeding"] = False
    game_state["blood_loss"] = 0
    character_stats["HP"] = character_stats["max_HP"]

    return

def check_passive_effects():
    """Check and apply passive effects that occur after every choice"""
    global previous_HP

    # ------------------------- HP Regen -----------------------------------
    if not game_state["has_hypothermia"] and not game_state["is_bleeding"] and (character_stats["HP"] < character_stats["max_HP"]) and (character_stats["HP"] >= previous_HP):
        HP_regain = game_state["time_healing"]
        character_stats["HP"] += HP_regain  # Passive HP regen when not affected by hypothermia or bleeding, increases the longer you go without taking damage
        game_state["time_healing"] += 1 # Increase after HP regain to ensure first turn is no healing


    # ------------------------- Mana Regen ---------------------------------

    if game_state.get("chosen_class") == 2:  # Mages get extra mana regen
        character_stats["Mana"] += 1
    character_stats["Mana"] += 1  # Passive mana regen

    # ------------------------- Hypothermia ---------------------------------

    if game_state["has_hypothermia"] and game_state["current_biome"] == "Tundra":
        character_stats["HP"] -= 1  # Hypothermia causes HP loss over time
        chance_to_heal = random.randint(1, 100)
        if chance_to_heal <= 20:  # 20% chance to heal hypothermia
            game_state["has_hypothermia"] = False
    elif game_state["has_hypothermia"] and game_state["current_biome"] != "Tundra":
        game_state["has_hypothermia"] = False  # Automatically heal hypothermia when leaving tundra

    # ------------------------ Bleeding -------------------------------------
    if game_state["is_bleeding"] and game_state["blood_loss"] <= 3:
        character_stats["HP"] -= (3 - game_state["blood_loss"])  # Bleeding causes HP loss over time, starting higher but getting smaller over time
        game_state["blood_loss"] += 1  # Blood loss increases over time

    elif game_state["is_bleeding"] and game_state["blood_loss"] > 3:
        game_state["is_bleeding"] = False
        game_state["blood_loss"] = 0  # Stop bleeding after a certain point to prevent infinite HP loss

    previous_HP = character_stats["HP"]  # Update previous HP for next turn comparisons

    return

def continue_if_dead(damage_taken):
    """Check if player has died from damage, and if so, save the player with either 1 or 2 remaining HP"""
    if damage_taken >= character_stats["HP"]:
        # Player would die - save them with 1 HP instead of dying
        before_damage = character_stats["HP"]
        character_stats["HP"] = random.randint(1, 2)
        actual_damage_taken = before_damage - character_stats["HP"]
        return actual_damage_taken  # Return the actual damage taken after saving from death
    
    return damage_taken  # No death, return original damage taken

def check_game_state():
    if character_stats["HP"] >= character_stats["max_HP"]:
        character_stats["HP"] = character_stats["max_HP"]
    if character_stats["Mana"] >= character_stats["max_Mana"]:
        character_stats["Mana"] = character_stats["max_Mana"]


    # To be updated, there will be a death screen and then a reset button, which will take you back to class selection
    if character_stats["HP"] <= 0:
        # Reset game state on death
        game_state["is_game_started"] = False
        game_state["current_biome"] = "Forest"
        character_stats["HP"] = 20
        character_stats["max_HP"] = 20
        character_stats["Mana"] = 20
        character_stats["max_Mana"] = 20
        character_stats["Energy"] = 100
        character_stats["Strength"] = 0
        character_stats["Defense"] = 0
        character_stats["Magic"] = 0
        character_stats["Dexterity"] = 0
        character_stats["Speed"] = 0
        character_stats["Swim"] = 0
        character_stats["Intellect"] = 0
        character_stats["XP"] = 0
        character_stats["Level"] = 1

def level_up():
    if character_stats["XP"] >= 100 * (character_stats["Level"] * 1.5):
        # Store old stats before leveling up
        old_level = character_stats["Level"]
        old_stats = {
            "HP": character_stats["max_HP"],
            "Mana": character_stats["max_Mana"],
            "Strength": character_stats["Strength"],
            "Defense": character_stats["Defense"],
            "Magic": character_stats["Magic"],
            "Dexterity": character_stats["Dexterity"],
            "Speed": character_stats["Speed"],
            "Swim": character_stats["Swim"],
            "Intellect": character_stats["Intellect"],
        }
        
        character_stats["Level"] += 1
        character_stats["XP"] = int(character_stats["XP"] - 100 * (old_level * 1.5))

        random_stat_increase = random.randint(0, 3)
        random_stat_increase_roll_two = random.randint(0, 3) # Reduce chances of increasing stats by taking the lower of 2 rolls

        if random_stat_increase_roll_two <= random_stat_increase:
            random_stat_increase

        for stat in character_stats:
            if stat in ["HP", "max_HP"]:
                increase = 0.75
                character_stats[stat] += math.floor(character_stats["Level"] * increase) # HP increases more with level to keep pace with stronger enemies
            
            elif stat in ["Mana", "max_Mana"]:
                increase = 0.5
                if game_state["chosen_class"] == 2:  # Mages get extra mana increase
                    increase = 1.0
                character_stats["max_Mana"] += math.floor(character_stats["Level"] * increase) # Mana increases more with level to keep pace with stronger spells
                
            elif stat in ["Strength", "Defense", "Magic"]:
                if game_state["chosen_class"] == 1 and stat == "Strength":  # Warriors get more strength increase
                    character_stats[stat] += random_stat_increase + 2 * math.ceil(character_stats["Level"] * 0.5)
                elif game_state["chosen_class"] == 2 and stat == "Magic":  # Mages get more magic increase
                    character_stats[stat] += random_stat_increase + 2 * math.ceil(character_stats["Level"] * 0.5)
                elif game_state["chosen_class"] == 3 and stat == "Defense":  # Defenders get more defense increase
                    character_stats[stat] += random_stat_increase + 2 * math.ceil(character_stats["Level"] * 0.5)
                else:
                    character_stats[stat] += random_stat_increase # Other stats increase more slowly with level to keep the game balanced

            elif stat in ["Dexterity", "Speed", "Swim", "Intellect"]:
                # New stats - increase gradually with each level
                character_stats[stat] += math.ceil(character_stats["Level"] * 0.3)

            elif stat in ["Energy"]:
                character_stats[stat] = 100

        character_stats["HP"] = character_stats["max_HP"]
        character_stats["Mana"] = character_stats["max_Mana"]

        # Calculate stat increases
        stat_increases = {
            "HP": character_stats["max_HP"] - old_stats["HP"],
            "Mana": character_stats["max_Mana"] - old_stats["Mana"],
            "Strength": character_stats["Strength"] - old_stats["Strength"],
            "Defense": character_stats["Defense"] - old_stats["Defense"],
            "Magic": character_stats["Magic"] - old_stats["Magic"],
            "Dexterity": character_stats["Dexterity"] - old_stats["Dexterity"],
            "Speed": character_stats["Speed"] - old_stats["Speed"],
            "Swim": character_stats["Swim"] - old_stats["Swim"],
            "Intellect": character_stats["Intellect"] - old_stats["Intellect"],
        }

        return {
            "text": f"LEVEL UP! You are now level {character_stats['Level']}!",
            "is_level_up": True,
            "new_level": character_stats["Level"],
            "stat_increases": stat_increases,
            "new_stats": {
                "HP": character_stats["max_HP"],
                "Mana": character_stats["max_Mana"],
                "Strength": character_stats["Strength"],
                "Defense": character_stats["Defense"],
                "Magic": character_stats["Magic"],
                "Dexterity": character_stats["Dexterity"],
                "Speed": character_stats["Speed"],
                "Swim": character_stats["Swim"],
                "Intellect": character_stats["Intellect"],
            },
            "continue": True
        }
    
    else:
        return {"text": "", "continue": True, "is_level_up": False}

def process_choice(event_name, choice):
    """Process player choice and return outcome"""
    
    # Check if there's a pending battle and player clicked "Fight!"
    if choice == "Fight!" and game_state.get("pending_battle_enemy"):
        enemy_type = game_state.pop("pending_battle_enemy")  # Remove the pending battle flag
        return start_battle(enemy_type)
    
    if event_name == "trigger_swamp_event":
        if choice == "Scavenge":
            fate = random.randint(1, 100)
            if fate <= 40:
                inventory["Wood"] += 2
                return {"text": "You found wood! Wood +2", "continue": True}
            elif fate <= 40:
                inventory["Iron"] += 2
                return {"text": "You found iron! Iron +2", "continue": True}
            elif fate <= 80:
                return start_battle_with_intro("Goblin", "You power through the swamp for some time before hearing something behind you. A goblin, right on your tail!")
            else:
                return {"text": "You found nothing of value.", "continue": True}
        elif choice == "Explore":
            fate = random.randint(1, 100)
            if fate <= 5:
                weapon_msg = get_random_weapon_by_rarity("Legendary")
                character_stats["XP"] += 10
                return {"text": f"You found a {weapon_msg}! Incredible! XP +10", "continue": True}
            elif fate <= 50:
                character_stats["XP"] += 5
                inventory["Wood"] += 1
                return {"text": "You explore deeper, before deciding to just grab some wood lying around. Wood +1, 5 XP!", "continue": True}
            elif fate <= 60:
                return start_battle_with_intro("Goblin", "As you explore, the ground beneath you starts to shake. Suddenly, a goblin jumps out from the water!")
            elif fate <= 80:
                teleport_random_biome()
                return {"text": "You find a hidden path that leads you safely out of the swamp.", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "You get  mosquito bites all over your body. Those are the worst creatures. HP -5", "continue": True}
        elif choice == "Rest":
            fate = random.randint(1, 2)
            if fate == 1:
                character_stats["HP"] = character_stats["max_HP"]
                return {"text": f"You rest and restore your HP to {character_stats['max_HP']}!", "continue": True}
            else:
                character_stats["HP"] -= 3
                return start_battle_with_intro("Siren", "As you rest, you hear what sounds ominously like a lullaby... You stand up, but are quickly attacked by a siren! You engage in battle, and lose HP from being jumped! HP -3")
    
    elif event_name == "trigger_gnome_ambush":
        if choice == "Spin Attack":
            fate = random.randint(1, 100)
            if character_stats["Strength"] >= (math.floor(character_stats["Level"] * 3)) and fate <= 40:
                character_stats["XP"] += 20
                character_stats["Strength"] += 1
                inventory["Money"] += 5
                return {"text": "You're so powerful, you simply spin and smash all of the gnomes, and they abandon their fallen brethren and the associated loot. XP +20, Strength +1, Money +5", "continue": True}
            elif character_stats["Strength"] >= (math.floor(character_stats["Level"] * 3)) and fate > 40:
                character_stats["XP"] += 5
                return {"text": "You manage to take out many gnomes with your spin attack, but there are too many of them. You run away like a coward. XP +5", "continue": True}
            elif character_stats["Strength"] < (math.floor(character_stats["Level"] * 3)) and fate <= 30:
                character_stats["XP"] += 5
                character_stats["HP"] -= 10
                return {"text": "You attempt a spin attack, and while you do manage to take out a gnome or two, you are quickly overwhelmed and beaten up. You do eventually defeat them, but are badly hurt. XP +5, HP -10", "continue": True}
            elif character_stats["Strength"] < (math.floor(character_stats["Level"] * 3)) and fate <= 65:
                character_stats["HP"] -= 20
                if character_stats["HP"] <= 0:
                    return {"text": "You think it's fun to try a spin attack on the gnomes. They do not. They eat you alive, and you are dead.", "continue": False}
                else:
                    return {"text": "You think it's fun to try a spin attack on the gnomes. They do not. They practically eat you alive, and leave you for dead. HP -20", "continue": True}
            else:
                character_stats["HP"] -= 5
                character_stats["Strength"] -= 1
                character_stats["Dexterity"] -= 1
                return {"text": "Your attack fails. The gnomes pity you and leave disappointedly. You are embarassed. XP -5, Dexterity -1, Strength -1", "continue": True}
        elif choice == "Lightning Strike":
            fate = random.randint(1, 100)
            if character_stats["Mana"] < 10:
                character_stats["HP"] -= 5
                return {"text": f"You don't have enough mana! You need 10 but only have {character_stats['Mana']}. The gnomes beat you up. HP -5", "continue": True}
            elif equipped_spell != "Lightning Bolt":
                character_stats["HP"] -= 5
                return {"text": f"You don't have the Lightning Bolt spell equipped, and are therefore incapable of doing a lightning strike. The gnomes beat you up. HP -5", "continue": True}
            elif character_stats["Magic"] > (math.ceil(character_stats["Level"] * 2.5)) and fate <= 50:
                character_stats["XP"] += 25
                character_stats["Mana"] -= 10
                return {"text": "Lightning strikes! Gnomes defeated. XP +25, Mana -10", "continue": True}
            elif character_stats["Magic"] > (math.ceil(character_stats["Level"] * 2.5)) and fate > 50:
                character_stats["XP"] += 5
                character_stats["Mana"] -= 10
                return {"text": "Your lightning strike is powerful, but there are just too many gnomes. You defeat some of them, but have to run away. XP +5, Mana -10", "continue": True}
            elif character_stats["Magic"] > 10:
                character_stats["HP"] -= 5
                return {"text": "You shoot a powerful lightning strike, but are unable to defeat all of the gnomes, and they overwhelm and trample you. You are lucky to have survived, but surprisingly didn't even get badly hurt. HP -5", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "You hold your hand out menacingly, as if to attempt casting a spell, but you're not that good at magic and fail. The gnomes beat you up. HP -5", "continue": True}
        elif choice == "Bribe":
            fate = random.randint(1, 100)
            if inventory["Money"] >= 2 and fate <= 65:
                inventory["Money"] -= 2
                return {"text": "You bribe the gnome king with your money, and he spares you. The gnomes continue on.", "continue": True}
            elif inventory["Money"] >= 2 and fate <= 67:
                return {"text": "The gnome king is impressed by your charm. He says some stuff in gnomish, and then brings out a pretty gnome girl. However, upon glancing at you, she seems unimpressed, and utters an \"ew\". You are destroyed.", "continue": False}
            elif inventory["Money"] >= 2 and fate <= 69:
                return {"text": "The gnome king is impressed by your charm. He says some stuff in gnomish, and then brings out a pretty gnome girl. She announces that she is the princess of the gnomes in your language. Long story short, you fall in love, she asks you to stay with her, and you choose not to continue on your journey. Traitor", "continue": False}
            elif inventory["Money"] >= 2 and fate <= 80:
                return {"text": "The gnome king is disappointed by your offer, but chooses to spare you. He leaves you with your cash, and you continue on", "continue": True}
            elif inventory["Money"] >= 2 and fate > 80:
                character_stats["HP"] -= 5
                return {"text": "You attempt to bargain with the gnome king, and eventually he gets bored of you and orders the gnomes to attack. They beat you up, but you're okay. HP -5"}
            elif fate <= 25:
                inventory["Money"] += 1
                return {"text": "Your bribe fails on account of not having enough money to meet the gnomes demands. Fortunately the gnome king is a good guy, and gives you some money to buy food. Money +1"}
            else:
                character_stats["HP"] -= 5
                return {"text": "You don't have enough money. The gnome king order his gnome armies to attack! They simply beat you up. Ouch. HP -5", "continue": True}
    
    elif event_name == "trigger_igloo_event":
        if choice == "Nap":
            fate = random.randint(1, 100)
            if fate <= 50:
                character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + 5)
                return {"text": "You take a refreshing nap, and nothing attacks you! You feel refreshed. HP +5", "continue": True}
            elif fate <= 80:
                game_state["has_hypothermia"] = True
                return {"text": "You take a nap, but the weather gets so cold, you end up catching hypothermia. HP -5", "continue": True}
            else:
                return start_battle_with_intro("Ice Golem", "You take a nap, but the cold awakens an ice golem that was dormant in the igloo. It is not happy to be woken up, and attacks you!")
        elif choice == "Melt Igloo":
            fate = random.randint(1, 100)
            if fate <= 40:
                inventory["Gold"] += 2
                character_stats["XP"] += 5
                return {"text": "You rummage around in the igloo and find some gold inside! Gold +2, XP +5", "continue": True}
            elif fate <= 75:
                return {"text": "You melt the igloo, but find nothing of value inside.", "continue": True}
            elif fate <= 90:
                character_stats["HP"] -= 5
                return {"text": "As you melt the igloo, you accidentally cause a small avalanche, and you end up caught in it. It definitely hurts a lot. HP -5", "continue": True}
            else:
                game_state["current_biome"] = "Ocean"
                return {"text": "You accidentally melted the entire tundra. You monster. You are now in an ocean.", "continue": True}
        elif choice == "Take Spell Book":
            fate = random.randint(1, 100)
            if fate <= 65:
                return {"text": "You take the book, but it's too old and faded to be of any use. You can't read it, and it crumbles to dust in your hands.", "continue": True}
            elif fate <= 80:
                character_stats["Magic"] += 2
                spell_msg = get_random_spell_of_type("Ice")
                return {"text": f"You took the book, and actually managed to learn something from it! Obtained {spell_msg}, Magic +2", "continue": True}
            else:
                game_state["has_hypothermia"] = True
                return {"text": "You grab the book, and slowly open it, expecting some incredible wisdom to emanate from the pages. In reality, the book is cursed and you catch hypothermia.", "continue": True}
    
    elif event_name == "trigger_cave_event":
        fate = random.randint(1, 100)
        if choice == "Venture In":
            if fate <= 25:
                character_stats["XP"] += 5
                return {"text": "You explore the cave, don't die, and even have some fun doing it! XP +5", "continue": True}
            if fate <= 50:
                return {"text": "You explore the cave, but sadly find nothing of value.", "continue": True}
            if fate <= 80:
                event_name = random.choice(["trigger_cave_2", "trigger_cave_3", "trigger_cave_4"])  # Trigger another cave event inside the cave for more exploration
                # Don't return here, just set the event name so that when the player makes their next choice, it will process the new cave event
            else:
                return start_battle_with_intro("Troll", "As you venture deeper into the cave, you disturb a cave troll that was sleeping. It is very angry and attacks you!")
        elif choice == "Camp Outside":
            if fate <= 50:
                character_stats["HP"] += 3
                return {"text": "Safe rest outside. HP +3", "continue": True}
            elif fate <= 80:
                return {"text": "You rest outside, but it's not very comfortable. You don't get much rest, but at least you're safe.", "continue": True}
            else:
                return start_battle_with_intro("Spider", "While sleeping, a giant spider sneaks out from the cave. You are awoken by the sounds of it attempting to destroy your tent, you must fight!")
        elif choice == "Leave":
            return {"text": "You decide it's too risky and move on.", "continue": True}

    elif event_name == "trigger_cave_2":
        if choice == "Go Deeper":
            fate = random.randint(1, 100)
            if fate <= 30:
                character_stats["XP"] += 10
                return {"text": "You find a hidden chamber with ancient writings on the walls. XP +10", "continue": True}
            elif fate <= 60:
                return {"text": "You find a small underground lake. It's beautiful, but there's nothing else of value here.", "continue": True}
            elif fate <= 85:
                character_stats["HP"] -= 5
                return {"text": "You slip on some wet rocks and hurt yourself. HP -5", "continue": True}
            else:
                return start_battle_with_intro("Giant Spider", "As you explore deeper into the cave, you disturb a giant spider's nest. The spider is very angry and attacks you!")
        elif choice == "Search for Resources":
            fate = random.randint(1, 100)
            if fate <= 40:
                inventory["Iron"] += 2
                return {"text": "You find some iron ore deposits in the cave! Iron +2", "continue": True}
            elif fate <= 80:
                return {"text": "You search around but only find some worthless rocks.", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "While searching, you accidentally knock over a rock pillar that falls on you. HP -5", "continue": True}
        elif choice == "Rest":
            fate = random.randint(1, 100)
            if fate <= 50:
                character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + 5)
                return {"text": f"You rest and restore your HP to {character_stats['max_HP']}!", "continue": True}
            else:
                return start_battle_with_intro("Cave Bat Swarm", "As you rest, you hear a high-pitched screeching sound. Suddenly, a swarm of cave bats descends upon you!")

    elif event_name == "trigger_cave_3":
        fate = random.randint(1, 100)
        if choice == "Investigate Noise":
            if fate <= 30:
                character_stats["XP"] += 10
                return {"text": "You find a hidden chamber with ancient writings on the walls. XP +10", "continue": True}
            elif fate <= 60:
                return {"text": "You find a small underground lake. It's beautiful, but there's nothing else of value here.", "continue": True}
            elif fate <= 85:
                character_stats["HP"] -= 5
                return {"text": "You slip on some wet rocks and hurt yourself. HP -5", "continue": True}
            else:
                enemy = random.choice(["Goblin", "Skeleton", "Spider"])
                return start_battle_with_intro(enemy, f"As you explore deeper into the cave, you disturb a {enemy}'s rest. The {enemy} hasn't eaten for days, and attacks you!")
        elif choice == "Fight!":
            enemy = random.choice(["Goblin", "Skeleton", "Spider"])
            return start_battle_with_intro(enemy, f"You bravely choose to fight whatever is making the noise. It turns out to be a {enemy} that attacks you!")
        elif choice == "Sneak Away":
            if fate <= 50:
                return {"text": "You successfully sneak away without being noticed.", "continue": True}
            else:
                enemy = random.choice(["Goblin", "Skeleton", "Spider"])
                return start_battle_with_intro(enemy, f"You try to sneak away, but accidentally make a noise that alerts a nearby {enemy}. It attacks you!")
            
    elif event_name == "trigger_cave_4":
        fate = random.randint(1, 100)
        if choice == "Go Deeper":
            if fate <= 30:
                character_stats["XP"] += 10
                character_stats["Intellect"] += 2
                return {"text": "You find a hidden chamber with ancient writings on the walls. You learn some valuable things. XP +10, Intellect +2", "continue": True}
            elif fate <= 60:
                return {"text": "You find a small underground lake. It's beautiful, but there's nothing else of value here.", "continue": True}
            elif fate <= 85:                
                character_stats["HP"] -= 5
                return {"text": "You slip on some wet rocks and hurt yourself. HP -5", "continue": True}
            else:
                return start_battle_with_intro("Troll", "You venture deeper into the cave and find a troll sleeping. You accidentally wake it up, and it is very angry and attacks you!")
        elif choice == "Search for Resources":
            if fate <= 40:
                inventory["Gold"] += 1
                return {"text": "You find a small vein of gold in the cave! Gold +1", "continue": True}
            elif fate <= 80:
                inventory["Iron"] += 1
                return {"text": "You find some iron in the cave! Iron +1", "continue": True}
            elif fate <= 90:
                weapon_msg = get_random_weapon_by_rarity("Exotic")
                while weapon_msg in game_state["player_weapons"]:
                    weapon_msg = get_random_weapon_by_rarity("Exotic")
                character_stats["XP"] += 5
                return {"text": f"You find a hidden stash of weapons in the cave! Almost none of them are still usable, but you still find a {weapon_msg} that's in good enough shape to use! XP +5", "continue": True}
            else:
                return start_battle_with_intro("Dragon", "You find a hidden chamber with ancient writings on the walls you attempt to read, but are incapable. In the darkness, you hear sudden movements, and as you turn, you see a dragon, awoken from a slumber. It comes right for you, and you defend yourself!")
        elif choice == "Rest":
            if fate <= 50:
                character_stats["HP"] += 1
                character_stats["Dexterity"] += 1
                return {"text": "You rest peacefully in the cave, undisturbed by any creatures. You feel refreshed. HP +1, Dexterity +1", "continue": True}
            elif fate <= 78:
                enemy = random.choice(["Goblin", "Skeleton", "Spider"])
                HP_loss = random.randint(1,5)
                character_stats["HP"] -= HP_loss
                return start_battle_with_intro(enemy, f"You rest in the cave, but are suddenly attacked by a {enemy} while trying to sleep. The {enemy} gets the first hit on you, inflicting {HP_loss} damage. Fight back, {game_state['chosen_class']}!")
            else:
                character_stats["HP"] += 3
                return {"text": "You rest safely in the cave. HP +3", "continue": True}
    
    elif event_name == "trigger_river_event":
        fate = random.randint(1, 100)
        if choice == "Swim":
            # If you have a good swim stat, these events will occur.
            if character_stats["Swim"] >= character_stats["Level"]:
                if fate <= 30:
                    damage_taken = continue_if_dead(5)
                    if damage_taken:
                        return {"text": f"Despite your swimming talent, the current of the river sweeps you far down the river. You hit the bottom of the river, are knocked out, but luckily awake on shore. HP -{damage_taken}", "continue": True}
                    else:
                        return {"text": "You might be a good swimmer, but the current was too strong. You didn't have enough health to survive being thrashed in the current, and you perish in the waves of the river.", "continue": False}
                elif fate <= 60:
                    character_stats["XP"] += 5
                    character_stats["Swim"] += 2
                    return {"text": "You successfully swim across the river without any issues, despite the wild current. Swim +2, XP +5", "continue": True}
                elif fate <= 80:
                    return start_battle_with_intro("Orc", "You swim across the river just fine, but on the other side of the river exists a group of orcs. You attempt to sneak away, but one notices you and comes to attack you!")
                else:
                    character_stats["XP"] += 5
                    return {"text": "You successfully swim across, the current was surprisingly not too strong. XP +5", "continue": True}
                
            # If your swim stat is too low, these events will occur
            if fate <= 30:
                damage_taken = continue_if_dead(10)
                if damage_taken:
                    return {"text": f"You attempt to swim across the river, but the current is too strong for you. You thrash around in the water, and eventually wash up on shore, exhausted and badly hurt. HP-{damage_taken}", "continue": True}
                else:
                    return {"text": f"You are incapable of swimming well enough to fight the current. The river drags you under, and claims you as a victim. You are slain", "continue": False}
            elif fate <= 50:
                character_stats["Swim"] += 1
                character_stats["XP"] += 5
                return {"text": "Despite some flailing around, the current is not too strong and you manage to get across without too much difficulty, only held back by your poor swimming skills. Luckily you learned something from this. Swim +1, XP +5", "continue": True}
            elif fate <= 55:
                return {"text": "You attempt to cross the river, but just drown.", "continue": False}
            elif fate <= 75:
                damage_taken = continue_if_dead(5)
                character_stats["HP"] -= damage_taken
                if damage_taken:
                    return start_battle_with_intro("Orc", f"You are swept away by the current, bashing your legs and arms along the river's floor. You take {damage_taken} damage, and are washed up on the shore. After regaining consciousness, you are attacked by an orc, and must immediately defend yourself!")
                else:
                    return {"text": "You are swept away by the current, and perish in river's depths.", "continue": False}
            else:
                damage_taken = continue_if_dead(3)
                if damage_taken:
                    game_state["is_bleeding"] = True
                    game_state["blood_lost"] = 0
                    character_stats["HP"] -= damage_taken
                    return {"text": "You manage to get across the river, but you scrape yourself up pretty bad. You are bleeding. HP -3", "continue": True}
                else:
                    return {"text": "You manage to get across the river, and somehow weren't even hurt in the process. You are tired, but can continue", "continue": True}
        elif choice == "Build Raft":
            character_stats["XP"] += 8
            return {"text": "You build a sturdy raft and cross safely. XP +8", "continue": True}
        elif choice == "Find Bridge":
            character_stats["XP"] += 3
            return {"text": "You find an old bridge. XP +3", "continue": True}
    
    elif event_name == "trigger_shipwreck_event":
        if choice == "Explore":
            inventory["Gold"] += 3
            return {"text": "You find treasure in the wreck! Gold +3", "continue": True}
        elif choice == "Search":
            return {"text": "No survivors found. The wreck has been abandoned for years.", "continue": True}
        elif choice == "Avoid":
            return {"text": "You wisely sail past the ominous wreck.", "continue": True}
    
    elif event_name == "trigger_desert_oasis":
        if choice == "Drink":
            character_stats["HP"] = character_stats["max_HP"]
            character_stats["Energy"] = 100
            return {"text": "Refreshing water! Full HP and Energy restored!", "continue": True}
        elif choice == "Camp":
            character_stats["HP"] += 10
            return {"text": "You rest at the oasis. HP +10", "continue": True}
        elif choice == "Continue":
            character_stats["HP"] -= 5
            return {"text": "The desert heat takes its toll. HP -5", "continue": True}
    
    elif event_name == "trigger_jungle_vines":
        if choice == "Cut":
            character_stats["XP"] += 5
            return {"text": "You cut through the vines. XP +5", "continue": True}
        elif choice == "Climb":
            if character_stats["Strength"] >= 10:
                character_stats["XP"] += 8
                return {"text": "You skillfully climb over! XP +8", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "You slip and fall. HP -5", "continue": True}
        elif choice == "Around":
            character_stats["XP"] += 2
            return {"text": "You find a path around. XP +2", "continue": True}
    
    elif event_name == "trigger_old_ruins":
        if choice == "Enter":
            character_stats["XP"] += 15
            return {"text": "You explore the ruins and discover ancient knowledge! XP +15", "continue": True}
        elif choice == "Search":
            inventory["Gold"] += 2
            return {"text": "You find ancient coins outside. Gold +2", "continue": True}
        elif choice == "Leave":
            return {"text": "The ruins seem too dangerous. You wisely move on.", "continue": True}
    
    elif event_name == "trigger_merchant_caravan":
        if choice == "Trade":
            if inventory["Gold"] > 0:
                inventory["Gold"] -= 1
                inventory["Money"] += 3
                return {"text": "Good trade! Gold -1, Money +3", "continue": True}
            else:
                return {"text": "You have nothing of value to trade.", "continue": True}
        elif choice == "Ask Directions":
            return {"text": "The merchant points you toward the next settlement.", "continue": True}
        elif choice == "Rob":
            if random.randint(1, 3) == 1:
                inventory["Gold"] += 5
                character_stats["HP"] -= 3
                return {"text": "You steal their gold but get caught! Gold +5, HP -3", "continue": True}
            else:
                character_stats["HP"] -= 10
                return {"text": "They fight back hard! HP -10", "continue": True}
    
    elif event_name == "trigger_pirate_attack":
        if game_state["chosen_class"] in [1, 3]:  # Warrior/Defender
            if choice == "Board Boat":
                character_stats["XP"] += 20
                return {"text": "You board the pirate ship! XP +20", "continue": True}
            elif choice == "Fire Cannon":
                character_stats["HP"] -= 10
                return {"text": "The pirates fire back! HP -10", "continue": True}
            elif choice == "Jump in Water":
                game_state["current_biome"] = "Forest"
                return {"text": "You swim to safety in a new biome!", "continue": True}
        else:  # Mage
            if choice == "Board Boat":
                character_stats["XP"] += 15
                return {"text": "You magically board the ship! XP +15", "continue": True}
            elif choice == "Conjure Storm":
                if character_stats["Mana"] < 10:
                    return {"text": f"You don't have enough mana! You need 10 but only have {character_stats['Mana']}. You are captured by pirates!", "continue": True}
                character_stats["Mana"] -= 10
                character_stats["XP"] += 25
                return {"text": "Powerful storm! Pirates flee! XP +25, Mana -10", "continue": True}
            elif choice == "Jump in Water":
                game_state["current_biome"] = "Plains"
                return {"text": "You escape to new lands!", "continue": True}
    
    elif event_name == "trigger_forest_encounter":
        if choice == "Attack":
            # Use weapon damage combined with strength to determine outcome
            player_power = get_total_player_power()
            gnome_difficulty = 35  # A little more difficult than easy
            fate = random.randint(1, 100)
            
            if player_power >= gnome_difficulty and fate <= 50:
                # Strong attack! Overwhelming victory
                character_stats["XP"] += 15
                weapon = get_equipped_weapon_data()
                weapon_name = equipped_weapon if equipped_weapon != "Fist" else "bare hands"
                return {"text": f"Your powerful strike with {weapon_name} overwhelms the gnomes! They are defeated. XP +15", "continue": True}
            elif player_power >= gnome_difficulty and fate <= 80:
                # Solid victory
                character_stats["XP"] += 12
                character_stats["HP"] -= 3
                return {"text": "You defeat the gnomes, but they put up a fight and manage to strike you a few times before going down. HP -3, XP +12", "continue": True}
            else:
                fate = random.randint(1, 100)
                # Standard victory
                if fate <= 70:
                    character_stats["XP"] += 10
                    character_stats["HP"] -= 5
                    return {"text": "You defeat the gnomes after a brief skirmish, but take some damage. HP -5, XP +10", "continue": True}
                else:
                    character_stats["HP"] -= 10
                    return {"text": "The gnomes outnumber you, and you take heavy damage before managing to escape! HP -10", "continue": True}
        elif choice == "Talk":
            character_stats["XP"] += 5
            fate = random.randint(1, 100)
            if fate <= 35:
                character_stats["Intellect"] += 1
                character_stats["XP"] += 5
                return {"text": "The gnomes appreciate your civility, and they teach you some important information. XP +5, Intellect +1", "continue": True}
            elif fate <= 60:
                return {"text": "The gnomes are indifferent to your attempts at conversation, but they let you be.", "continue": True}
            elif fate <= 80:
                damage_taken = random.randint(1, 5)
                character_stats["HP"] -= damage_taken
                return {"text": f"The gnomes turn violent, and begin to attack you. You aren't too badly harmed, but take {damage_taken} damage.", "continue": True}
            else:
                return {"text": "The gnomes are amused by your attempts at conversation, and they decide to let you go on your way.", "continue": True}
        elif choice == "Run":
            fate = random.randint(1, 100)
            if character_stats["Speed"] >= 5 and fate <= 55:
                return {"text": "You escape into the forest...", "continue": True}
            elif character_stats["Speed"] >= 5 and fate <= 70:
                character_stats["HP"] -= 2
                return {"text": "You manage to escape, but not before the gnomes strike you a few times. HP -2", "continue": True}
            elif character_stats["Speed"] >= 5:
                character_stats["HP"] -= 3
                character_stats["Speed"] += 1
                return {"text": "The gnomes are fast, and you struggle to get away. You take some damage, but have learned to run a bit quicker. Speed +1, HP -3", "continue": True}
            elif character_stats["Speed"] < 5:
                if fate <= 50:
                    return {"text": "You try to run, but the gnomes are too fast! You manage to escape, but not before taking significant damage. HP -10", "continue": True}
                else:
                    character_stats["Speed"] += 2
                    return {"text": "You're not much of a runner, but you're at least faster than the gnomes. In fact, you might just be a little faster in general. Speed +2", "continue": True}
            else:
                damage_taken = random.randint(1, 5)
                character_stats["HP"] -= damage_taken
                return {"text": f"You try to run, but the gnomes are too fast! You take {damage_taken} damage.", "continue": True}
    
    elif event_name == "trigger_goblin_fight":
        if choice == "Fight":
            character_stats["XP"] += 15
            return {"text": "You defeat the goblin! XP +15", "continue": True}
        elif choice == "Cast Spell":
            if character_stats["Mana"] < 5:
                return {"text": f"You don't have enough mana! You need 5 but only have {character_stats['Mana']}. The goblin attacks! HP -10", "continue": True}
            character_stats["Mana"] -= 5
            character_stats["XP"] += 12
            return {"text": "Spell hits! XP +12, Mana -5", "continue": True}
        elif choice == "Flee":
            return {"text": "You safely flee.", "continue": True}
    
    elif event_name == "trigger_ancient_tomb":
        if choice == "Take Weapon":
            fate = random.randint(1, 100)
            if fate <= 50:
                weapon_msg = get_random_weapon_by_rarity("Uncommon")
                character_stats["XP"] += 10
                return {"text": f"{weapon_msg}\nXP +10", "continue": True}
            if fate <= 60:
                weapon_msg = weapon_get("Shadow Katana")
                character_stats["XP"] += 25
                return {"text": f"{weapon_msg}\nXP +25", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "You approach the sword, but trigger a trap! HP -5", "continue": True}
        elif choice == "Search Treasure":
            if equipped_weapon == "Shadow Katana":
                fate = random.randint(1, 100)
                if fate <= 70:
                    inventory["Gold"] += 5
                    return {"text": "You see an ancient lock, and insert your shadow katana to open up to a vault! Unfortunately, it appears to have mostly been raided. You still get some money. Gold +5", "continue": True}
                else:
                    return {"text": "You see an ancient lock, and insert your shadow katana to open up to a vault! Tragically, it appears to be empty.", "continue": True}
            else:
                return {"text": "You search the tomb but find nothing of value. Maybe there's a hidden mechanism that requires a special weapon?", "continue": True}
        elif choice == "Leave":
            fate = random.randint(1, 2)
            if fate == 1:
                return {"text": "You leave the tomb undisturbed.", "continue": True}
            elif fate == 2:
                return {"text": "You escape the tomb without too much difficulty", "continue": True}
    
    elif event_name == "trigger_blacksmith_forge":
        if choice == "Take Weapon":
            weapon_msg = weapon_get("Flame Mace")
            character_stats["XP"] += 20
            return {"text": f"{weapon_msg}\nXP +20", "continue": True}
        elif choice == "Talk":
            return {"text": "A ghostly voice thanks you for respecting the forge. You feel stronger. STR +2", "continue": True}
        elif choice == "Leave":
            character_stats["XP"] += 5
            return {"text": "You respectfully leave. XP +5", "continue": True}
    
    elif event_name == "trigger_dragon_nest":
        if choice == "Grab Gold":
            fate = random.randint(1, 100)
            if fate <= 30:
                inventory["Gold"] += 10
                return {"text": "You collect treasure from the nest. Gold +10", "continue": True}
            else:
                return start_battle_with_intro("Dragon", "As you reach for the gold, a massive dragon swoops down to defend its nest! Prepare for battle!")
        elif choice == "Take Egg":
            fate = random.randint(1, 100)
            if fate <= 20:
                inventory["Gold"] += 3
                character_stats["XP"] += 50
                return {"text": "You take the dragon egg! A baby dragon bursts forth - XP +50, Gold +3", "continue": True}
            if fate <= 35:
                weapon_msg = weapon_get("Dragon Claw")
                return {"text": f"You go in for the egg, but find something even better! {weapon_msg}", "continue": True}
            elif fate <= 75:
                return start_battle_with_intro("Dragon", "The dragon is enraged that you tried to steal its egg! It attacks with fiery fury!")
            else:
                character_stats["HP"] -= 20
                return {"text": "The dragon is furious and attacks you! You can't even defend yourself in time, so you run, but not before taking substantial damage. HP -20", "continue": True}
        elif choice == "Flee":
            fate = random.randint(1, 100)
            if fate <= 60:
                return {"text": "You flee as the dragon returns!", "continue": True}
            else:
                return start_battle_with_intro("Dragon", "You try to flee, but are not fast enough. Prepare to fight for your life!")
    
    elif event_name == "trigger_cursed_library":
        if choice == "Touch Artifact":
            fate = random.randint(1, 2)
            if fate == 1:
                weapon_msg = weapon_get("Cursed Dagger")
                return {"text": f"The artifact grants you a weapon! {weapon_msg}", "continue": True}
            else:
                character_stats["HP"] -= 10
                return {"text": "The artifact curses you! HP -10", "continue": True}
        elif choice == "Read Books":
            character_stats["Magic"] += 3
            return {"text": "You learn ancient magic. Magic +3", "continue": True}
        elif choice == "Run":
            return {"text": "You escape safely.", "continue": True}
    
    elif event_name == "trigger_lost_temple":
        if choice == "Walk Carefully":
            character_stats["XP"] += 30
            inventory["Gold"] += 8
            return {"text": "You navigate the traps perfectly! XP +30, Gold +8", "continue": True}
        elif choice == "Smash Through":
            character_stats["HP"] -= 15
            inventory["Gold"] += 5
            return {"text": "Traps trigger! HP -15, but you grab Gold +5", "continue": True}
        elif choice == "Mark Exit":
            return {"text": "You safely mark a path and return to explore later.", "continue": True}
    
    elif event_name == "trigger_crystal_cave":
        if choice == "Harvest":
            inventory["Gold"] += 4
            character_stats["XP"] += 10
            return {"text": "The crystals shimmer and transform into gold! Gold +4, XP +10", "continue": True}
        elif choice == "Meditate":
            character_stats["Mana"] = character_stats["max_Mana"]
            character_stats["HP"] += 5
            return {"text": "The crystals heal you. Mana restored, HP +5", "continue": True}
        elif choice == "Leave":
            return {"text": "You leave the beautiful cave.", "continue": True}
    
    elif event_name == "trigger_phoenix_shrine":
        if choice == "Show Respect":
            weapon_msg = weapon_get("Phoenix Staff")
            character_stats["XP"] += 35
            return {"text": f"The phoenix blesses you! {weapon_msg}\nXP +35", "continue": True}
        elif choice == "Grab":
            character_stats["HP"] -= 20
            inventory["Gold"] += 3
            return {"text": "The phoenix attacks you! HP -20, but you grab Gold +3", "continue": True}
        elif choice == "Run":
            return {"text": "You flee the shrine safely.", "continue": True}
    
    elif event_name == "trigger_goblin_settlement":
        if choice == "Sneak":
            fate = random.randint(1, 2)
            if fate == 1:
                weapon_msg = weapon_get("Iron Sword")
                return {"text": f"You steal a weapon! {weapon_msg}", "continue": True}
            else:
                character_stats["HP"] -= 8
                return {"text": "You get caught! HP -8", "continue": True}
        elif choice == "Trade":
            if inventory["Gold"] > 0:
                inventory["Gold"] -= 1
                inventory["Money"] += 5
                return {"text": "Fair trade! Gold -1, Money +5", "continue": True}
            else:
                return {"text": "You have nothing to trade.", "continue": True}
        elif choice == "Attack":
            character_stats["XP"] += 20
            return {"text": "You defeat several goblins! XP +20", "continue": True}
    
    elif event_name == "trigger_wizard_tower":
        if choice == "Climb":
            character_stats["XP"] += 15
            return {"text": "You climb the tower and meet the wizard. XP +15", "continue": True}
        elif choice == "Magic":
            if character_stats["Magic"] >= 5:
                weapon_msg = weapon_get("Scepter of Stars")
                character_stats["Magic"] += 2
                return {"text": f"The wizard recognizes your power! {weapon_msg}\nMagic +2", "continue": True}
            else:
                return {"text": "The wizard ignores you.", "continue": True}
        elif choice == "Ignore":
            return {"text": "You ignore the tower and move on.", "continue": True}
    
    elif event_name == "trigger_sunken_ruin":
        if choice == "Dive":
            fate = random.randint(1, 2)
            if fate == 1:
                inventory["Gold"] += 7
                return {"text": "You find treasure underwater! Gold +7", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "You struggle in the water! HP -5", "continue": True}
        elif choice == "Call Help":
            return {"text": "Nobody comes to help you. You mark the location.", "continue": True}
        elif choice == "Mark Map":
            character_stats["XP"] += 8
            return {"text": "You map out the ruins. XP +8", "continue": True}
    
    elif event_name == "trigger_dark_forest":
        if choice == "Investigate":
            fate = random.randint(1, 3)
            if fate == 1:
                return {"text": "Shadow creatures attack you! HP -10", "continue": True}
            elif fate == 2:
                weapon_msg = weapon_get("Wraith Scythe")
                return {"text": f"You find a mystical weapon! {weapon_msg}", "continue": True}
            else:
                character_stats["XP"] += 20
                return {"text": "You discover ancient knowledge! XP +20", "continue": True}
        elif choice == "Light Fire":
            character_stats["XP"] += 10
            return {"text": "The light frightens the creatures away. XP +10", "continue": True}
        elif choice == "Leave":
            return {"text": "You wisely leave the dark forest.", "continue": True}

    elif event_name == "trigger_ice_fishing":
        if choice == "Swim":
            character_stats["HP"] -= 5
            return {"text": "You swim in the icy water and get cold! HP -5", "continue": True}
        elif choice == "Fish":
            fate = random.randint(1, 2)
            if fate == 1:
                inventory["Fish"] += 1
                return {"text": "You catch a fish! Fish +1", "continue": True}
            else:
                return {"text": "You don't catch anything.", "continue": True}
        elif choice == "Enjoy View":
            character_stats["XP"] += 5
            return {"text": "You enjoy the view. XP +5", "continue": True}
        
    elif event_name == "trigger_ancient_grove":
        if choice == "Listen":
            character_stats["XP"] += 15
            return {"text": "The trees share their wisdom! XP +15", "continue": True}
        elif choice == "Gather":
            inventory["Herbs"] += 1
            return {"text": "You gather medicinal herbs! Herbs +1", "continue": True}
        elif choice == "Rest":
            character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + 10)
            return {"text": "The grove heals you. HP +10", "continue": True}
        
    elif event_name == "trigger_woman_encounter":
        if choice == "Approach":
            fate = random.randint(1, 100)
            if fate <= 15:
                character_stats["Morale"] += 10
                return {"text": "The woman turns out to be nice, you have a nice chat. Morale +10", "continue": True}
            elif fate <= 25:
                return {"text": "The woman turns out to be a siren, lures you into the water, and you drown. Game Over.", "continue": False}
            else:
                character_stats["HP"] -= 15
                return {"text": "The woman turns out to be a siren and lures you into the water. You nearly drown, but escape.", "continue": True}
        elif choice == "Strike":
            character_stats["HP"] -= 10
            return {"text": "The woman is startled and attacks you! HP -10", "continue": True}
        elif choice == "Ignore":
            return {"text": "You ignore the woman and continue on your way.", "continue": True}

    elif event_name == "trigger_orc_battle":
        # Any choice leads to battle with the Orc
        return start_battle("Orc")
    
    elif event_name == "trigger_biome_transition":
        if choice == "Leave":
            new_biome = random.choice(BIOMES)
            game_state["current_biome"] = new_biome
            return {"text": f"You continue on and enter the {new_biome}...", "continue": True}
        elif choice == "Stay":
            return {"text": f"You choose to remain in the {game_state['current_biome']}.", "continue": True}
        
    elif event_name == "trigger_arrow_to_the_knee":
        if choice == "Keep Going":
            fate = random.randint(1, 2)
            if character_stats["Dexterity"] >= (character_stats["Level"] * 3) and fate == 1:
                return {"text": "You manage to keep going without much trouble!", "continue": True}
            if character_stats["Strength"] >= (character_stats["Level"] * 3) and fate == 1:
                character_stats["HP"] += 1
                return {"text": "You decide to continue, and your strength snaps the arrow out of your leg. You feel good as new! HP +1", "continue": True}
            elif fate == 1:
                character_stats["HP"] -= 5
                return {"text": "You manage to keep going despite the pain. HP -5", "continue": True}
            if fate == 2:
                character_stats["Intellect"] += 1
                return {"text": "You analyze the situation and find a way to minimize the pain. Intellect +1", "continue": True}
            character_stats["HP"] -= 5
            return {"text": "You keep going despite the pain. HP -5", "continue": True}
        elif choice == "Rest":
            fate = random.randint(1, 100)
            if fate <= 25:
                character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + 10)
                return {"text": "You rest and tend to your wound. HP +10", "continue": True}
            else:
                return start_battle_with_intro("Orc", "You take a moment to rest. In your moment of weakness, an orc ambushes you! Prepare for battle!")
        elif choice == "Seek Healer":
            fate = random.randint(1, 100)
            if fate < 25:
                character_stats["XP"] += 10
                character_stats["HP"] = character_stats["max_HP"]
                return {"text": "You seek out a healer, who heals you. HP restored, XP +10", "continue": True}
            elif fate < 35:
                character_stats["max_HP"] -= 2
                character_stats["HP"] -= 5
                return {"text": "You are too far from any potential help, you are in pain. Max_HP -2, HP -5", "continue": True}
            elif fate <= 55:
                # Encounter an Orc disguised as a healer! Show intro, then battle
                return start_battle_with_intro("Orc", "You finally find someone who claims to be a healer. As you approach, they suddenly reveal themselves—an Orc! They draw their weapon, ready for combat.")
            elif fate <= 75:
                # Take damage from the pain
                character_stats["HP"] -= 20
                return {"text": "You search for a healer but the pain is too much to bear, you manage to rip the arrow out but it deals some severe damage. HP -20", "continue": True}
            elif fate <= 80:
                # Find a random rare weapon from a dead adventurer
                rare_weapon = get_random_weapon_by_rarity("Rare")
                weapon_msg = weapon_get(rare_weapon)
                return {"text": f"While searching for a healer, you're surprised to notice that it wasn't an arrow in your knee at all. {weapon_msg}!", "continue": True}
            else:
                return {"text": "You search for a healer but find none. However, you hardly feel any pain anymore. Guess walking it off was all you needed.", "continue": True}
        
        # Place new events before this line ^^^
        
    return {"text": "Unknown choice", "continue": True}


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get current character stats"""
    return jsonify(character_stats)

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    """Get current inventory"""
    return jsonify({
        "resources": inventory,
        "weapons": player_weapons,
        "spells": player_spells,
        "equipped_weapon": equipped_weapon,
        "equipped_spell": equipped_spell,
    })

@app.route("/api/game-state", methods=["GET"])
def get_game_state():
    """Get overall game state"""
    return jsonify({
        "game_state": game_state,
        "stats": character_stats,
        "inventory": inventory,
        "weapons": player_weapons,
        "spells": player_spells,
        "equipped_weapon": equipped_weapon,
        "equipped_spell": equipped_spell,
    })

# ==================== COMBAT ENDPOINTS ====================

@app.route("/api/start-combat", methods=["POST"])
def start_combat():
    """Start a combat encounter with level-scaled enemy stats"""
    global player_spells
    
    data = request.json
    enemy_type = data.get("enemy_type", "Goblin")
    
    if enemy_type not in ENEMIES_DB:
        enemy_type = "Goblin"
    
    # Get scaled enemy stats based on player level
    enemy_data = scale_enemy_stats(enemy_type, character_stats["Level"])
    enemy_hp = random.randint(enemy_data["hp"][0], enemy_data["hp"][1])
    
    game_state["in_combat"] = True
    game_state["current_enemy"] = enemy_type
    game_state["current_enemy_hp"] = enemy_hp
    game_state["current_enemy_max_hp"] = enemy_hp
    
    # Give starting spells if player has none
    if not player_spells and game_state["chosen_class"] == 2:
        player_spells = {"Wind Spell": SPELLS_DB["Wind Spell"]}
    
    return jsonify({
        "status": "combat_started",
        "enemy": enemy_type,
        "enemy_hp": enemy_hp,
        "player_hp": character_stats["HP"],
        "message": f"⚔️ A fierce {enemy_type} appears! Prepare for combat! ⚔️",
    })

@app.route("/api/combat-attack", methods=["POST"])
def combat_attack():
    """Handle combat attack action"""
    data = request.json
    action_type = data.get("type")  # "weapon" or "spell"
    action_name = data.get("action")
    
    if not game_state["in_combat"]:
        return jsonify({"error": "Not in combat"}), 400
    
    enemy_type = game_state["current_enemy"]
    # Get scaled enemy stats based on player level
    enemy_data = scale_enemy_stats(enemy_type, character_stats["Level"])
    
    result_text = ""
    player_damage = 0
    
    # Player attack
    if action_type == "weapon":
        if action_name not in player_weapons:
            return jsonify({"error": "Weapon not found"}), 400
        
        weapon_data = player_weapons[action_name]
        # allow using the equipped weapon by passing "equipped"
        if action_name == "equipped":
            action_name = equipped_weapon
            weapon_data = player_weapons.get(action_name, weapon_data)

        # base damage from weapon + strength/dexterity modifiers
        base = random.randint(weapon_data["damage"][0], weapon_data["damage"][1])
        strength_bonus = math.floor(character_stats.get("Strength", 0) * 0.6)
        dex_bonus = math.floor(character_stats.get("Dexterity", 0) * 0.3)
        player_damage = max(0, base + strength_bonus + dex_bonus)

        # check for weapon special power and apply if exists
        special_power_result = weapon_special_power()
        if special_power_result and "special_power" in special_power_result.get_json():
            enemy_status_effect = special_power_result.get_json().get("effect", None)
            
            if enemy_status_effect == "ice":
                game_state["frozen_effect"] = {
                    "damage": special_power_result.get_json().get("frozen_damage", 0),
                    "turns_left": 1
                }
            result_text += special_power_result.get_json()["message"] + "\n"

        # hit chance modified by dexterity
        hit_roll = random.randint(1, 100)
        hit_threshold = weapon_data.get("hit_chance", 75) + min(20, character_stats.get("Dexterity", 0) // 2)
        if hit_roll <= hit_threshold:
            result_text += f"🗡️ You hit with {action_name}! Damage: {player_damage}\n"
            game_state["current_enemy_hp"] -= player_damage
        else:
            result_text += f"❌ Your {action_name} missed!\n"
    
    elif action_type == "spell":
        # allow using the equipped spell by passing "equipped"
        if action_name == "equipped":
            action_name = equipped_spell

        if action_name not in player_spells:
            return jsonify({"error": "Spell not found"}), 400

        spell_data = player_spells[action_name]

        if character_stats["Mana"] < spell_data["mana_cost"]:
            return jsonify({"error": f"Not enough mana! Need {spell_data['mana_cost']}, have {character_stats['Mana']}"}), 400

        character_stats["Mana"] -= spell_data["mana_cost"]

        base = random.randint(spell_data["damage"][0], spell_data["damage"][1])
        magic_bonus = math.floor(character_stats.get("Magic", 0) * 0.7)
        int_bonus = math.floor(character_stats.get("Intellect", 0) * 0.4)
        player_damage = max(0, base + magic_bonus + int_bonus)

        # check for spell special effect and apply if exists
        special_effect_result = spell_special_effect()
        if special_effect_result and "special_effect" in special_effect_result.get_json():
            spell_status_effect = special_effect_result.get_json().get("effect", None)
            burn_damage = special_effect_result.get_json().get("burn_damage", 0)
            if spell_status_effect == "burn":
                # apply burn damage over time effect to enemy
                game_state["burn_effect"] = {
                    "damage": burn_damage,
                    "turns_left": random.randint(1, 5)
                }

        # spell hit chance modified by intellect
        hit_roll = random.randint(1, 100)
        hit_threshold = spell_data.get("hit_chance", 75) + min(20, character_stats.get("Intellect", 0) // 2)
        if hit_roll <= hit_threshold:
            result_text += f"✨ {action_name} hits! Damage: {player_damage}\n"
            game_state["current_enemy_hp"] -= player_damage
        else:
            result_text += f"❌ {action_name} missed!\n"
    
    # Enemy counter-attack
    if game_state["current_enemy_hp"] > 0:
        enemy_damage = random.randint(enemy_data["damage"][0], enemy_data["damage"][1])
        enemy_hit = random.randint(1, 100)
        
        # Defense reduces damage
        defense_reduction = max(0, character_stats["Defense"] // 2)
        enemy_damage = max(1, enemy_damage - defense_reduction)
        
        if enemy_hit > 20:  # Enemies have 80% hit chance
            character_stats["HP"] -= enemy_damage
            result_text += f"💥 {enemy_type} attacks! Damage: {enemy_damage}\n"
        else:
            result_text += f"⚔️ {enemy_type} misses!\n"
    
    # Check combat end
    combat_end = False
    end_message = ""
    
    if game_state["current_enemy_hp"] <= 0:
        combat_end = True
        xp_gain = enemy_data["xp_reward"]
        money_gain = random.randint(enemy_data["money_reward"][0], enemy_data["money_reward"][1])
        
        character_stats["XP"] += xp_gain
        inventory["Money"] += money_gain
        
        end_message = f"🎉 Victory! {enemy_type} defeated!\nXP +{xp_gain}, Money +{money_gain}"
        game_state["in_combat"] = False
    
    elif character_stats["HP"] <= 0:
        combat_end = True
        character_stats["HP"] = 0
        end_message = "💀 You have been defeated..."
        game_state["in_combat"] = False
    
    return jsonify({
        "combat_active": game_state["in_combat"],
        "player_hp": character_stats["HP"],
        "player_mana": character_stats["Mana"],
        "enemy_hp": max(0, game_state["current_enemy_hp"]),
        "action_text": result_text,
        "combat_end": combat_end,
        "end_message": end_message,
        "game_over": character_stats["HP"] <= 0,
    })

@app.route("/api/weapon-special-power", methods=["POST"])
def weapon_special_power():
    """Use a weapon's special power"""
    global equipped_weapon

    data = request.json
    weapon_name = data.get("weapon")

    if weapon_name not in player_weapons:
        return jsonify({"error": "Weapon not found"}), 400

    weapon_data = player_weapons[weapon_name]
    special_power = weapon_data.get("special_power", None)

    if not special_power:
        return jsonify({"error": ""}), 400

    if special_power == "Ice":
        # Special power: Ice - chance to freeze enemy in combat
        if game_state["in_combat"]:
            freeze_chance = 30 + character_stats.get("Intellect", 0) // 2
            if random.randint(1, 100) <= freeze_chance:
                return jsonify({
                    "message": f"{weapon_name}'s {special_power} triggered! Enemy is frozen and misses their next turn!",
                    "special_power": special_power,
                    "effect": "freeze"
                })
            else:
                return jsonify({
                    "message": f"",
                    "special_power": special_power,
                    "effect": None
                })
    
    if special_power == "Fire":
        # Special power: Fire - chance to burn enemy for damage over time
        if game_state["in_combat"]:
            burn_chance = 25 + character_stats.get("Magic", 0) // 2
            if random.randint(1, 100) <= burn_chance:
                burn_damage = 5 + character_stats.get("Magic", 0) // 3
                return jsonify({
                    "message": f"{weapon_name}'s {special_power} triggered! Enemy is burned and takes {burn_damage} damage over time!",
                    "special_power": special_power,
                    "effect": "burn",
                    "burn_damage": burn_damage
                })

    return jsonify({
        "message": f"",
        "special_power": None
    })

@app.route("/api/spell-special-effect", methods=["POST"])
def spell_special_effect():
    """Apply a spell's special effect"""
    global equipped_spell

    data = request.json
    spell_name = data.get("spell")

    if spell_name not in player_spells:
        return jsonify({"error": "Spell not found"}), 400

    spell_data = player_spells[spell_name]
    special_effect = spell_data.get("special_effect", None)

    if not special_effect:
        return jsonify({"error": ""}), 400

    if special_effect == "Heal":
        # Special effect: Heal - restores HP when used in combat
        if game_state["in_combat"]:
            heal_amount = 10 + character_stats.get("Magic", 0) // 2
            character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + heal_amount)
            return jsonify({
                "message": f"{spell_name}'s {special_effect} triggered! You heal for {heal_amount} HP!",
                "special_effect": special_effect,
                "heal_amount": heal_amount
            })

    return jsonify({
        "message": f"{spell_name}'s {special_effect} triggered!",
        "special_effect": special_effect
    })

@app.route("/api/equip-weapon", methods=["POST"])
def equip_weapon():
    """Equip a different weapon"""
    global equipped_weapon
    
    data = request.json
    weapon_name = data.get("weapon")
    
    # If weapon is known in the global DB but not yet in player's weapons, allow adding it
    if weapon_name not in player_weapons:
        if weapon_name in WEAPONS_DB:
            player_weapons[weapon_name] = WEAPONS_DB[weapon_name]
        else:
            return jsonify({"error": "Weapon not found"}), 400

    equipped_weapon = weapon_name
    return jsonify({"equipped": weapon_name, "weapons": player_weapons})

@app.route("/api/equip-spell", methods=["POST"])
def equip_spell():
    """Equip a different spell"""
    global equipped_spell
    
    data = request.json or {}
    spell_name = data.get("spell")
    print("\n" + "="*60)
    print("🔧 EQUIP-SPELL ENDPOINT CALLED")
    print(f"   Spell name requested: {spell_name}")
    print(f"   Player spells: {list(player_spells.keys())}")
    print(f"   Currently equipped: {equipped_spell}")
    print("="*60 + "\n")

    # If no spell provided, allow unequipping
    if not spell_name:
        equipped_spell = None
        print("   → Unequipping spell")
        return jsonify({"equipped": None, "spells": player_spells})

    # If the player doesn't have the spell but it exists in global DB, grant it (learn it)
    if spell_name not in player_spells:
        if spell_name in SPELLS_DB:
            player_spells[spell_name] = SPELLS_DB[spell_name]
            print(f"   → Added {spell_name} from SPELLS_DB to player inventory")
        else:
            print(f"   → ERROR: {spell_name} not found in SPELLS_DB")
            return jsonify({"error": "Spell not found"}), 400

    equipped_spell = spell_name
    print(f"   → SUCCESS: Equipped spell is now: {equipped_spell}")
    print(f"   → Returning spells: {list(player_spells.keys())}\n")
    return jsonify({"equipped": spell_name, "spells": player_spells})


# ==================== REACT DEV SERVER PROXY ====================
# Catch-all route: proxy to React dev server for all non-API requests
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy_to_react(path):
    """Proxy non-API requests to React dev server on localhost:3000"""
    # Don't proxy API routes - they're handled above
    if path.startswith("api/"):
        return jsonify({"error": "Not Found"}), 404
    
    try:
        # Build the target URL
        target_url = f"{REACT_DEV_SERVER}/{path}"
        
        # Forward the request to React dev server
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for key, value in request.headers if key != "Host"},
            data=request.get_data(),
            allow_redirects=False
        )
        
        # Return the response from React dev server
        return response.content, response.status_code, dict(response.headers)
    except requests.exceptions.ConnectionError:
        # If React dev server is not running, return helpful message
        return jsonify({"error": "React dev server not running on localhost:3000. Please run 'npm start' in the frontend folder."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🎮 Adventure Game Backend Server")
    print("=" * 50)
    print("API Server running on: http://localhost:5000")
    print("Proxying UI requests to: http://localhost:3000")
    print("=" * 50)
    print("\n📝 To run the complete game:")
    print("   Terminal 1: npm start (in frontend folder)")
    print("   Terminal 2: python backend/app.py (in backend folder)")
    print("   Then visit: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)
