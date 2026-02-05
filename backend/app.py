from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import json
import os

app = Flask(__name__, static_folder="../", static_url_path="")
CORS(app)

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
    # Legendary
    "Reaper of the Gods": {"rarity": "Legendary", "damage": [80, 95], "hit_chance": 90, "type": "Melee", "special_power": "blind"},
    "Sun Blade": {"rarity": "Legendary", "damage": [50, 60], "hit_chance": 80, "type": "Melee", "special_power": "fire"},
    "Dragon Fang": {"rarity": "Legendary", "damage": [85, 100], "hit_chance": 75, "type": "Melee", "special_power": "poison"},
    "Hammer of Titans": {"rarity": "Legendary", "damage": [90, 110], "hit_chance": 65, "type": "Melee", "special_power": "stun"},
    "Blade of Eternity": {"rarity": "Legendary", "damage": [95, 120], "hit_chance": 85, "type": "Melee", "special_power": "stun"},
    # Rare
    "Bright Blade": {"rarity": "Rare", "damage": [20, 25], "hit_chance": 75, "type": "Melee", "special_power": "blind"},
    "Storm Bow": {"rarity": "Rare", "damage": [25, 35], "hit_chance": 80, "type": "Ranged", "special_power": "shock"},
    "Shadow Katana": {"rarity": "Rare", "damage": [28, 40], "hit_chance": 75, "type": "Melee", "special_power": "curse"},
    "Flame Mace": {"rarity": "Rare", "damage": [30, 45], "hit_chance": 65, "type": "Melee", "special_power": "fire"},
    # Uncommon
    "Bronze Sword": {"rarity": "Uncommon", "damage": [14, 20], "hit_chance": 70, "type": "Melee", "special_power": "none"},
    "Iron Mace": {"rarity": "Uncommon", "damage": [16, 22], "hit_chance": 60, "type": "Melee", "special_power": "none"},
    # Common
    "Iron Sword": {"rarity": "Common", "damage": [10, 20], "hit_chance": 60, "type": "Melee", "special_power": "none"},
    "Wooden Club": {"rarity": "Common", "damage": [6, 12], "hit_chance": 65, "type": "Melee", "special_power": "none"},
    "Fist": {"rarity": "None", "damage": [3, 3], "hit_chance": 70, "type": "Melee", "special_power": "none"},
}

SPELLS_DB = {
    # Wind
    "Wind Spell": {"damage": [5, 8], "hit_chance": 95, "mana_cost": 1, "special_power": "none"},
    "Gust": {"damage": [8, 15], "hit_chance": 70, "mana_cost": 2, "special_power": "none"},
    # Ice
    "Ice Blast": {"damage": [10, 20], "hit_chance": 60, "mana_cost": 3, "special_power": "ice"},
    "Frost Spike": {"damage": [15, 25], "hit_chance": 65, "mana_cost": 4, "special_power": "ice"},
    # Lightning
    "Lightning Bolt": {"damage": [15, 20], "hit_chance": 75, "mana_cost": 3, "special_power": "stun"},
    "Thunder Strike": {"damage": [20, 30], "hit_chance": 65, "mana_cost": 5, "special_power": "stun"},
    # Fire
    "Fireball": {"damage": [15, 25], "hit_chance": 65, "mana_cost": 4, "special_power": "fire"},
    "Flame Wave": {"damage": [20, 30], "hit_chance": 60, "mana_cost": 5, "special_power": "fire"},
    # Holy
    "Holy Beam": {"damage": [15, 25], "hit_chance": 75, "mana_cost": 4, "special_power": "heal"},
    "Healing Light": {"damage": [0, 0], "hit_chance": 100, "mana_cost": 6, "special_power": "heal"},
}

# Enemy definitions
ENEMIES_DB = {
    "Goblin": {"hp": [15, 25], "damage": [3, 8], "xp_reward": 20, "money_reward": [5, 15]},
    "Orc": {"hp": [30, 50], "damage": [8, 15], "xp_reward": 50, "money_reward": [20, 40]},
    "Dragon": {"hp": [100, 150], "damage": [20, 40], "xp_reward": 200, "money_reward": [100, 200]},
    "Pirate": {"hp": [20, 35], "damage": [5, 12], "xp_reward": 30, "money_reward": [15, 30]},
    "Dark Knight": {"hp": [50, 80], "damage": [15, 25], "xp_reward": 100, "money_reward": [50, 100]},
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

# ==================== EVENTS ====================
# Event functions return (text, choices)

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

# Event pool by biome
EVENTS = {
    "Forest": [trigger_gnome_ambush, trigger_old_ruins, trigger_forest_encounter, trigger_ancient_tomb, trigger_crystal_cave, trigger_dark_forest],
    "Ocean": [trigger_pirate_attack, trigger_shipwreck_event, trigger_sunken_ruin],
    "Plains": [trigger_river_event, trigger_merchant_caravan, trigger_goblin_fight, trigger_goblin_settlement],
    "Swamp": [trigger_swamp_event, trigger_cursed_library],
    "Tundra": [trigger_igloo_event, trigger_lost_temple],
    "Mountain": [trigger_cave_event, trigger_blacksmith_forge, trigger_wizard_tower],
    "Desert": [trigger_desert_oasis, trigger_dragon_nest],
    "Jungle": [trigger_jungle_vines, trigger_phoenix_shrine],
}

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

# ==================== ROUTES ====================

@app.route("/api/init", methods=["POST"])
def init_game():
    """Initialize a new game with character class selection"""
    global equipped_weapon, equipped_spell, player_weapons, player_spells
    
    data = request.json
    chosen_class = data.get("chosen_class")  # 1, 2, or 3
    
    game_state["chosen_class"] = chosen_class
    game_state["is_game_started"] = True
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
    
    text, choices = selected_event()
    event_name = selected_event.__name__
    
    game_state["current_event_name"] = event_name
    
    return jsonify({
        "event_name": event_name,
        "text": text,
        "choices": choices,
    })

@app.route("/api/choose", methods=["POST"])
def handle_choice():
    """Handle player's choice in an event"""
    data = request.json
    choice = data.get("choice")
    event_name = data.get("event_name")
    
    # Determine outcome based on event and choice
    outcome = process_choice(event_name, choice)
    
    return jsonify(outcome)

def process_choice(event_name, choice):
    """Process player choice and return outcome"""
    
    if event_name == "trigger_swamp_event":
        if choice == "Scavenge":
            fate = random.randint(1, 3)
            if fate == 1:
                inventory["Wood"] += 1
                return {"text": "You found wood! Wood +1", "continue": True}
            elif fate == 2:
                inventory["Iron"] += 1
                return {"text": "You found iron! Iron +1", "continue": True}
            else:
                return {"text": "You found nothing of value.", "continue": True}
        elif choice == "Explore":
            character_stats["XP"] += 5
            return {"text": "You explore deeper and gain 5 XP!", "continue": True}
        elif choice == "Rest":
            character_stats["HP"] = character_stats["max_HP"]
            return {"text": f"You rest and restore your HP to {character_stats['max_HP']}!", "continue": True}
    
    elif event_name == "trigger_gnome_ambush":
        if choice == "Spin Attack":
            if character_stats["Strength"] >= 15:
                character_stats["XP"] += 20
                inventory["Money"] += 5
                return {"text": "Perfect spin attack! Defeated gnomes. XP +20, Money +5", "continue": True}
            else:
                character_stats["HP"] -= 5
                return {"text": "Your attack fails. HP -5. The gnomes pity you and leave.", "continue": True}
        elif choice == "Lightning Strike":
            character_stats["XP"] += 25
            character_stats["Mana"] = max(0, character_stats["Mana"] - 10)
            return {"text": "Lightning strikes! Gnomes defeated. XP +25, Mana -10", "continue": True}
        elif choice == "Bribe":
            if inventory["Money"] >= 2:
                inventory["Money"] -= 2
                return {"text": "You bribe the gnome king. Money -2. You live!", "continue": True}
            else:
                return {"text": "You don't have enough money. The gnomes attack!", "continue": True}
    
    elif event_name == "trigger_igloo_event":
        if choice == "Nap":
            character_stats["HP"] = min(character_stats["max_HP"], character_stats["HP"] + 5)
            return {"text": "Refreshing nap! HP +5", "continue": True}
        elif choice == "Melt Igloo":
            if random.randint(1, 2) == 1:
                inventory["Gold"] += 2
                character_stats["XP"] += 5
                return {"text": "Found gold inside! Gold +2, XP +5", "continue": True}
            else:
                game_state["current_biome"] = "Ocean"
                return {"text": "You accidentally melted the entire tundra area and fell into the ocean!", "continue": True}
        elif choice == "Take Spell Book":
            character_stats["Magic"] += 2
            return {"text": "You took the icicle spell book! Magic +2", "continue": True}
    
    elif event_name == "trigger_cave_event":
        if choice == "Venture In":
            character_stats["XP"] += 10
            return {"text": "You explore the cave and find ancient treasures! XP +10", "continue": True}
        elif choice == "Camp Outside":
            character_stats["HP"] += 3
            return {"text": "Safe rest outside. HP +3", "continue": True}
        elif choice == "Leave":
            return {"text": "You decide it's too risky and move on.", "continue": True}
    
    elif event_name == "trigger_river_event":
        if choice == "Swim":
            if random.randint(1, 3) == 1:
                character_stats["HP"] -= 5
                return {"text": "Strong current! You nearly drown. HP -5", "continue": True}
            else:
                character_stats["XP"] += 5
                return {"text": "You successfully swim across! XP +5", "continue": True}
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
                character_stats["Mana"] -= 10
                character_stats["XP"] += 25
                return {"text": "Powerful storm! Pirates flee! XP +25, Mana -10", "continue": True}
            elif choice == "Jump in Water":
                game_state["current_biome"] = "Plains"
                return {"text": "You escape to new lands!", "continue": True}
    
    elif event_name == "trigger_forest_encounter":
        if choice == "Attack":
            character_stats["XP"] += 10
            return {"text": "You defeat the gnomes! XP +10", "continue": True}
        elif choice == "Talk":
            character_stats["XP"] += 5
            return {"text": "The gnomes appreciate your civility. XP +5", "continue": True}
        elif choice == "Run":
            return {"text": "You escape into the forest...", "continue": True}
    
    elif event_name == "trigger_goblin_fight":
        if choice == "Fight":
            character_stats["XP"] += 15
            return {"text": "You defeat the goblin! XP +15", "continue": True}
        elif choice == "Cast Spell":
            character_stats["Mana"] -= 5
            character_stats["XP"] += 12
            return {"text": "Spell hits! XP +12, Mana -5", "continue": True}
        elif choice == "Flee":
            return {"text": "You safely flee.", "continue": True}
    
    elif event_name == "trigger_ancient_tomb":
        if choice == "Take Weapon":
            weapon_msg = weapon_get("Shadow Katana")
            character_stats["XP"] += 25
            return {"text": f"{weapon_msg}\nXP +25", "continue": True}
        elif choice == "Search Treasure":
            inventory["Gold"] += 5
            return {"text": "You find ancient gold coins. Gold +5", "continue": True}
        elif choice == "Leave":
            return {"text": "You leave the tomb undisturbed.", "continue": True}
    
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
            inventory["Gold"] += 10
            return {"text": "You collect treasure from the nest. Gold +10", "continue": True}
        elif choice == "Take Egg":
            inventory["Gold"] += 3
            character_stats["XP"] += 50
            return {"text": "You take the dragon egg! A baby dragon bursts forth - XP +50, Gold +3", "continue": True}
        elif choice == "Flee":
            return {"text": "You flee as the dragon returns!", "continue": True}
    
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
    """Start a combat encounter"""
    global player_spells
    
    data = request.json
    enemy_type = data.get("enemy_type", "Goblin")
    
    if enemy_type not in ENEMIES_DB:
        enemy_type = "Goblin"
    
    enemy_data = ENEMIES_DB[enemy_type]
    enemy_hp = random.randint(enemy_data["hp"][0], enemy_data["hp"][1])
    
    game_state["in_combat"] = True
    game_state["current_enemy"] = enemy_type
    game_state["current_enemy_hp"] = enemy_hp
    
    # Give starting spells if player has none
    if not player_spells and game_state["chosen_class"] == 2:
        player_spells = {"Wind Spell": SPELLS_DB["Wind Spell"]}
    
    return jsonify({
        "status": "combat_started",
        "enemy": enemy_type,
        "enemy_hp": enemy_hp,
        "player_hp": character_stats["HP"],
        "message": f"A {enemy_type} appears! Prepare for combat!",
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
    enemy_data = ENEMIES_DB[enemy_type]
    
    result_text = ""
    player_damage = 0
    
    # Player attack
    if action_type == "weapon":
        if action_name not in player_weapons:
            return jsonify({"error": "Weapon not found"}), 400
        
        weapon_data = player_weapons[action_name]
        player_damage = random.randint(weapon_data["damage"][0], weapon_data["damage"][1])
        hit_roll = random.randint(1, 100)
        
        if hit_roll <= weapon_data["hit_chance"]:
            result_text += f"🗡️ You hit with {action_name}! Damage: {player_damage}\n"
            game_state["current_enemy_hp"] -= player_damage
        else:
            result_text += f"❌ Your {action_name} missed!\n"
    
    elif action_type == "spell":
        if action_name not in player_spells:
            return jsonify({"error": "Spell not found"}), 400
        
        spell_data = player_spells[action_name]
        
        if character_stats["Mana"] < spell_data["mana_cost"]:
            return jsonify({"error": f"Not enough mana! Need {spell_data['mana_cost']}, have {character_stats['Mana']}"}), 400
        
        character_stats["Mana"] -= spell_data["mana_cost"]
        player_damage = random.randint(spell_data["damage"][0], spell_data["damage"][1])
        hit_roll = random.randint(1, 100)
        
        if hit_roll <= spell_data["hit_chance"]:
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
        
        if enemy_hit > 30:  # Enemies have 70% hit chance
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
    })

@app.route("/api/equip-weapon", methods=["POST"])
def equip_weapon():
    """Equip a different weapon"""
    global equipped_weapon
    
    data = request.json
    weapon_name = data.get("weapon")
    
    if weapon_name not in player_weapons:
        return jsonify({"error": "Weapon not found"}), 400
    
    equipped_weapon = weapon_name
    return jsonify({"equipped": weapon_name})

@app.route("/api/equip-spell", methods=["POST"])
def equip_spell():
    """Equip a different spell"""
    global equipped_spell
    
    data = request.json
    spell_name = data.get("spell")
    
    if spell_name and spell_name not in player_spells:
        return jsonify({"error": "Spell not found"}), 400
    
    equipped_spell = spell_name
    return jsonify({"equipped": spell_name})

if __name__ == "__main__":
    print("🎮 Adventure Game Backend running on http://localhost:5000")
    app.run(debug=True, port=5000)
