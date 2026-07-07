game_state = {
    "player_name": "Hero",
    "chosen_class": None,  # 1=Warrior, 2=Mage, 3=Defender
    "current_biome": "Forest",
    "is_game_started": False,
    "current_event_name": None,
    "in_combat": False,
    "current_enemy": None,
    "current_enemy_hp": 0,
    "current_enemy_max_hp": 0,
    "enemy_speed": 0,
    "minigame": None,

    # Combat session tracking
    "combat_session": {
        "turn_count": 0,
        "player_turn": True,
        "combat_log": [],
    },

    # Status effects positive
    "time_healing": 0,

    # Status effects negative
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

# Base inventory, items may be appended throughout game. These items will always display regardless of amount.
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

# Generic items acquired outside weapons/spells/resources
player_items = {}

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
    "Blade of Blackbeard": {"rarity": "Legendary", "damage": random.randint(80, 120), "hit_chance": 90, "type": "Melee", "drop_rate": 1, "special_power": "none"},

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

ITEMS_DB = {
    "Wood": {
        "type": "resource",
        "rarity": "Common",
        "amount_range": [1, 3],
        "messages": [
            "You gather a few logs of wood.",
            "You scavenge some dry timber.",
            "A small pile of wood falls into your arms."
        ]
    },
    "Iron": {
        "type": "resource",
        "rarity": "Uncommon",
        "amount_range": [1, 2],
        "messages": [
            "You uncover a few iron ingots.",
            "You find iron ore along the path.",
            "A lump of iron clinks into your pack."
        ]
    },
    "Gold": {
        "type": "resource",
        "rarity": "Rare",
        "amount_range": [1, 3],
        "messages": [
            "You discover a glint of gold.",
            "You pry a few gold nuggets out of the dirt.",
            "A small cache of gold jingles into your hand."
        ]
    },
    "Money": {
        "type": "resource",
        "rarity": "Common",
        "amount_range": [3, 8],
        "messages": [
            "You find loose coins on the ground.",
            "A small pouch of money falls into your hand.",
            "You pick up some extra cash."
        ]
    },
    "Healing Herb": {
        "type": "item",
        "rarity": "Common",
        "amount_range": [1, 1],
        "messages": [
            "You find a healing herb.",
            "A medicinal plant grows nearby.",
            "You pocket a useful herb."
        ]
    },
    "Mana Crystal": {
        "type": "item",
        "rarity": "Uncommon",
        "amount_range": [1, 1],
        "messages": [
            "You discover a glowing mana crystal.",
            "A crystal hums with arcane energy.",
            "You pick up a small burst of magic power."
        ]
    },
    "Ancient Scroll": {
        "type": "item",
        "rarity": "Rare",
        "amount_range": [1, 1],
        "messages": [
            "You uncover an ancient scroll.",
            "A dusty scroll flutters free from the ground.",
            "You recover a mysterious writ."
        ]
    },
    "Crystal Shard": {
        "type": "item",
        "rarity": "Uncommon",
        "amount_range": [1, 2],
        "messages": [
            "You mine a sparkling crystal shard.",
            "A small crystal shard falls into your hand.",
            "You find a glowing fragment of crystal."
        ]
    },
    "Lucky Charm": {
        "type": "item",
        "rarity": "Rare",
        "amount_range": [1, 1],
        "messages": [
            "You find a lucky charm.",
            "A strange talisman glows faintly.",
            "You pocket a small good-luck charm."
        ]
    }
}

RARITY_WEIGHTS = {
    "Common": 60,
    "Uncommon": 25,
    "Rare": 10,
    "Legendary": 5,
}

# Enemy definitions - base stats without scaling
ENEMIES_DB = {
    "Goblin": {"hp": [15, 25], "damage": [3, 5], "xp_reward": 5, "money_reward": [1, 3], "level_scaling": 0.4, "status_effect": None},
    "Orc": {"hp": [30, 50], "damage": [4, 6], "xp_reward": 10, "money_reward": [2, 5], "level_scaling": 0.8, "status_effect": None},
    "Dragon": {"hp": [100, 150], "damage": [8, 10], "xp_reward": 20, "money_reward": [8, 15], "level_scaling": 1.5, "status_effect": None},
    "Pirate": {"hp": [20, 35], "damage": [3, 5], "xp_reward": 30, "money_reward": [2, 5], "level_scaling": 0.5, "status_effect": None},
    "Siren": {"hp": [50, 80], "damage": [4, 7], "xp_reward": 50, "money_reward": [3, 7], "level_scaling": 1.0, "status_effect": None},
    "Ice Golem": {"hp": [60, 90], "damage": [2, 4], "xp_reward": 20, "money_reward": [5, 6], "level_scaling": 1.0, "status_effect": None},
    "Troll": {"hp": [40, 70], "damage": [3, 7], "xp_reward": 20, "money_reward": [2, 5], "level_scaling": 0.9, "status_effect": None},
    "Skeleton": {"hp": [25, 45], "damage": [2, 4], "xp_reward": 10, "money_reward": [1, 3], "level_scaling": 0.6, "status_effect": None},
    "Spider": {"hp": [10, 20], "damage": [2, 5], "xp_reward": 5, "money_reward": [1, 3], "level_scaling": 0.3, "status_effect": None},
    "Cursed Spirit": {"hp": [20, 30], "damage": [4, 8], "xp_reward": 5, "money_reward": [0, 1], "level_scaling": 0.8, "status_effect": "Curse"},

    # Bosses
    "Great Sage": {"hp": [250, 350], "damage": [10, 35], "xp_reward": 100, "money_reward": [15, 20], "level_scaling": 1.0, "status_effect": None},
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
        enemy_type = "Spider" if "spider" in str(enemy_type).lower() else "Goblin"
    
    game_state["in_combat"] = True
    scaled_enemy = scale_enemy_stats(enemy_type, character_stats["Level"])
    enemy_hp = random.randint(scaled_enemy["hp"][0], scaled_enemy["hp"][1])
    
    game_state["current_enemy"] = enemy_type
    game_state["current_enemy_hp"] = enemy_hp
    game_state["current_enemy_max_hp"] = enemy_hp
    game_state["enemy_skip_turns"] = 0
    
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
        enemy_type = "Spider" if "spider" in str(enemy_type).lower() else "Goblin"
    
    # Store pending battle info
    game_state["pending_battle_enemy"] = enemy_type
    
    return {
        "event_name": "battle_intro",
        "text": narrative,
        "choices": ["Fight!"],
        "battle_intro": True,
        "continue": False
    }

def start_bowling(narrative):
    """Start a bowling minigame for the player."""
    game_state["minigame"] = "bowling"
    return {
        "minigame": "bowling",
        "text": narrative,
    }

# ==================== COMBAT MANAGEMENT FUNCTIONS ====================

def reset_combat_session():
    """Reset combat session for a new battle"""
    game_state["combat_session"] = {
        "turn_count": 0,
        "player_turn": True,
        "combat_log": [],
    }

def determine_turn_order():
    """Determine who goes first based on speed stats. Returns True if player goes first."""
    player_speed = character_stats.get("Speed", 0)
    enemy_type = game_state.get("current_enemy", "Goblin")
    enemy_data = scale_enemy_stats(enemy_type, character_stats["Level"])
    
    # Add some randomness to speed (±10%)
    player_effective_speed = player_speed * (random.uniform(0.9, 1.1))
    enemy_effective_speed = 10 * (random.uniform(0.9, 1.1))  # Base enemy speed
    
    return player_effective_speed >= enemy_effective_speed

def initialize_combat(enemy_type):
    """Initialize a new combat encounter with proper speed-based turn order"""
    if enemy_type not in ENEMIES_DB:
        enemy_type = "Goblin"
    
    # Reset combat session
    reset_combat_session()
    
    # Setup enemy
    game_state["in_combat"] = True
    scaled_enemy = scale_enemy_stats(enemy_type, character_stats["Level"])
    enemy_hp = random.randint(scaled_enemy["hp"][0], scaled_enemy["hp"][1])
    
    game_state["current_enemy"] = enemy_type
    game_state["current_enemy_hp"] = enemy_hp
    game_state["current_enemy_max_hp"] = enemy_hp
    game_state["enemy_speed"] = 10  # Base enemy speed
    
    # Determine initial turn order
    player_goes_first = determine_turn_order()
    game_state["combat_session"]["player_turn"] = player_goes_first
    
    # Initialize combat log
    turn_order_message = "You move first!" if player_goes_first else f"{enemy_type} moves first!"
    game_state["combat_session"]["combat_log"].append(f"⚔️ COMBAT STARTED!\n{turn_order_message}")
    
    return {
        "enemy": enemy_type,
        "enemy_hp": enemy_hp,
        "enemy_max_hp": enemy_hp,
        "player_goes_first": player_goes_first,
        "player_speed": character_stats.get("Speed", 0),
    }

def end_combat(victory=True):
    """End combat and reset session"""
    if victory:
        enemy_type = game_state.get("current_enemy", "Unknown")
        enemy_data = scale_enemy_stats(enemy_type, character_stats["Level"])
        xp_gain = enemy_data["xp_reward"]
        money_gain = random.randint(enemy_data["money_reward"][0], enemy_data["money_reward"][1])
        
        increase_XP(xp_gain)
        inventory["Money"] += money_gain
        
        result = {
            "victory": True,
            "xp_gain": xp_gain,
            "money_gain": money_gain,
            "message": f"🎉 Victory! {enemy_type} defeated!\nXP +{xp_gain}, Money +{money_gain}"
        }
    else:
        result = {
            "victory": False,
            "message": "💀 You have been defeated... Game Over."
        }
    
    game_state["in_combat"] = False
    game_state["current_enemy"] = None
    game_state["current_enemy_hp"] = 0
    game_state["current_enemy_max_hp"] = 0
    reset_combat_session()
    
    return result
