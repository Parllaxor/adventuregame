# This is an action style adventure game where you make choices that influence an outcome.
# Devin Coombs

import random
import sys
import math
import time

def print_choices(choice_list):
    print(choice_list[0])
    print(choice_list[1])
    print(choice_list[2])
    print("")
    return

# Pre-enabled Conditions and Stats

max_HP = 20
max_Mana = 20
critical_chance = 15
is_Victorious = False
is_On_Water = False

def print_stats():
    print(character_statistics)
    return

def check_inventory():
    print(inventory)
    return

def print_enemy_stats():
    print(enemy_stats)
    return

def level_up():
    if chosen_class == 1:
        preferred_stat = "Strength"
    elif chosen_class == 2:
        preferred_stat = "Magic"
    elif chosen_class == 3:
        preferred_stat = "Defense"
    else:
        preferred_stat = "Strength"

    # Keep leveling up if enough XP
    while character_statistics["XP"] >= character_statistics["Level"] * math.ceil(10 * character_statistics["Level"]):
        OldLevel = character_statistics["Level"]
        OldStrength = character_statistics["Strength"]
        OldMagic = character_statistics["Magic"]
        OldDefense = character_statistics["Defense"]
        OldSwim = character_statistics["Swim"]
        OldSpeed = character_statistics["Speed"]

        # Spend XP & level up first
        required_XP = character_statistics["Level"] * math.ceil(10 * character_statistics["Level"])
        character_statistics["XP"] -= required_XP
        character_statistics["Level"] += 1

        # Preferred stat bonus (always at least +1)
        character_statistics[preferred_stat] += random.randint(1, math.ceil(character_statistics[preferred_stat] * 0.25))

        # Bonus stats depending on level
        if character_statistics["Level"] % 2 == 0:
            character_statistics["Strength"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))
            character_statistics["Speed"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
        if character_statistics["Level"] % 3 == 0:
            character_statistics["Magic"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))
            character_statistics["Swim"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
        if character_statistics["Level"] % 5 == 0:
            character_statistics["Defense"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))

        if character_statistics["Level"] % 4 == 0:  
            # Energy boost sometimes 
            if random.randint(1, 100) < 30:
                character_statistics["Energy"] = 100

        if character_statistics["Level"] % 3 == 0:
            # Morale boost sometimes
            if random.randint(1, 100) < 30:
                character_statistics["Morale"] = 100

        # Print level up summary
        print(f"""
        LEVEL UP!
   Level: {OldLevel} ---> {character_statistics["Level"]}
Strength: {OldStrength} ---> {character_statistics["Strength"]}
 Defense: {OldDefense} ---> {character_statistics["Defense"]}
   Magic: {OldMagic} ---> {character_statistics["Magic"]}
   Speed: {OldSpeed} ---> {character_statistics["Speed"]}
    Swim: {OldSwim} ---> {character_statistics["Swim"]}""")

def does_game_end():
    # check if game ends
    if character_statistics["HP"] <= 0:
        print("""You take too much damage, and are unable to continue. 
Game Over.""")
        sys.exit()
    elif character_statistics["Morale"] <= 0:
        print("""Your morale has reached the lowest of lows. Maybe this whole adventuring thing isn't really for you.
        You give up.""")
        sys.exit()
    elif character_statistics["Energy"] <= 0:
        print("""You collapse from exhaustion. 
Game Over.""")
        sys.exit()

    # check stats overflow and reset
    if character_statistics["HP"] > max_HP:
        character_statistics["HP"] = max_HP
    elif character_statistics["Morale"] > 100:
        character_statistics["Morale"] = 100
    elif character_statistics["Energy"] > 100:
        character_statistics["Energy"] = 100
    else:
        return
    
def teleport_random_biome():
    global Csetting
    setting[Csetting] = False
    while(True):
        new_random_biome = random.randint(1, 8)
        if new_random_biome == 1 and Csetting != "Forest":
            Csetting = "Forest"
            break
        elif new_random_biome == 2 and Csetting != "Swamp":
            Csetting = "Swamp"
            break
        elif new_random_biome == 3 and Csetting != "Plains":
            Csetting = "Plains"
            break
        elif new_random_biome == 4 and Csetting != "Ocean":
            Csetting = "Ocean"
            break
        elif new_random_biome == 5 and Csetting != "Tundra":
            Csetting = "Tundra"
            break
        elif new_random_biome == 6 and Csetting != "Jungle":
            Csetting = "Jungle"
            break
        elif new_random_biome == 7 and Csetting != "Desert":
            Csetting = "Desert"
            break
        elif new_random_biome == 8 and Csetting != "Mountains":
            Csetting = "Mountains"
            break
        
    setting[Csetting] = True
    print(f"""
You have arrived in the {Csetting}.
""")
    return

def enter_setting(NewSetting):
    global Csetting
    setting[Csetting] = False
    Csetting = NewSetting
    setting[Csetting] = True
    print(f"""
You have arrived in the {Csetting}.
""")
    return

def check_morale_HP():
    if character_statistics["Morale"] >= 100:
        character_statistics["Morale"] = 100
    if character_statistics["HP"] >= max_HP:
        character_statistics["HP"] = max_HP
    if character_statistics["Energy"] >= 100:
        character_statistics["Energy"] = 100

    return

    # Combat

# Damage to enemy
def calculate_damage(attack_type, weapon_damage, strike_chance):
    if is_hit(strike_chance) == False:
        print("""Your attack missed!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
        return
    if attack_type.lower() == "melee":
        damage_dealt = ((character_statistics["Strength"] * 0.25) * weapon_damage) - enemy_stats["Defense"]
    elif attack_type.lower() == "magic":
        damage_dealt = ((character_statistics["Magic"] * 0.5) * weapon_damage) - enemy_stats["Magic"]
    elif attack_type.lower() == "throw":
        damage_dealt = ((character_statistics["Strength"] * 0.5) * weapon_damage) - enemy_stats["Defense"]
    elif attack_type.lower() == "ranged":
        damage_dealt = ((character_statistics["Dexterity"] * 3) * weapon_damage) - enemy_stats["Defense"]
    elif damage_dealt <= 0:
        damage_dealt = 1
    else:
        return

    if damage_dealt < weapon_damage:
        damage_dealt = weapon_damage

    is_crit = is_critical_hit()
    if is_crit == True:
        print("Critical hit!")
        enemy_stats["HP"] -= (2*damage_dealt)
        return math.ceil(2*(damage_dealt))
    else:
        enemy_stats["HP"] -= math.ceil(damage_dealt)
        return math.ceil(damage_dealt)

def is_critical_hit():
    if random.randint(1, 100) <= critical_chance:
        return True
    else:
        return False
    
def is_hit(strike_chance):
    if random.randint(1, 100) <= strike_chance:
        return True
    else:
        return False
    
def is_valid_item(choice, item_lookup):
    # This function is to determine whether or not an item selected by the user to use can be used in combat.

    try:
        choice = int(choice)
    except ValueError:
        print("Invalid choice — not a number.")
        return

    if choice == 1:
        return

    if choice in item_lookup:
        item = item_lookup[choice]
        if item.lower() == "wood":
            print("""""")
            # Do wood-related logic here
        elif item.lower() == "gold":
            # Throw gold at enemy
            if random.randint(1, 100) < character_statistics["Speed"] * (character_statistics["Strength"] + character_statistics["Magic"]):
                damage = calculate_damage("throw", random.randint(1, 10), 1)
                print(f"""You chuck a piece of gold at the enemy, dealing {damage} damage""")
                enemy_stats["HP"] -= damage
            else:
                print("""You throw the gold at the enemy, but you completely miss.""")
        elif item.lower() == "rubber ducks":
            print("Quack! Rubber ducks selected")
            # Do rubber duck logic here
    else:
        print("Invalid choice — number not in menu.")
    return

def is_valid_weapon(choice):
    choice = choice.strip().title()

    weapon_stats = weapons.get(choice)
    if not weapon_stats:
        print("Invalid weapon! (GAME BUG)")
        return

    # Calculate damage
    damage = calculate_damage(
        weapon_stats["type"],
        weapon_stats["damage"],
        weapon_stats["hit_chance"]
    )
    if damage is None:
        return

    # Print attack message
    if enemy_stats["HP"] >= 0:
        print(f"""You attack with your {choice} dealing {damage} damage. 
The enemy has {enemy_stats['HP']} HP left.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
    else:
        print(f"""You attack with your {choice} dealing {damage} damage. 
The enemy has been slain.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

    # Handle special power (if any)
    if weapon_stats.get("special_power") and weapon_stats["special_power"] != "none":
        print(f"The {choice} unleashes its special power: {weapon_stats['special_power'].capitalize()}!")
        special_power(weapon_stats['special_power'].lower())


def is_valid_spell(choice):
    choice = choice.strip().title()

    spell_stats = spells.get(choice)
    if not spell_stats:
        print("Invalid weapon! (GAME BUG)")
        return

    # Calculate damage
    damage = calculate_damage("magic",spell_stats["damage"],spell_stats["hit_chance"])
    if damage is None:
        return

    # Print attack message
    if enemy_stats["HP"] >= 0:
        print(f"""You attack with your {choice} dealing {damage} damage. 
The enemy has {enemy_stats['HP']} HP left.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
    else:
        print(f"""You attack with your {choice} dealing {damage} damage. 
The enemy has been slain.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

    # Handle special power (if any)
    if spell_stats.get("special_power") and spell_stats["special_power"] != "none":
        print(f"The {choice} unleashes its special power: {spell_stats['special_power'].capitalize()}!")
        special_power(spell_stats['special_power'].lower())


def special_power(power):
    if power == "fire":
        print("""The enemy is burning.""")


def enemy_dead(combat_opponent, enemy_level):
    if combat_opponent.lower() == "hydra":
        xp = enemy_level * math.ceil(random.randint(10, 20))
        character_statistics["XP"] += xp
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "goblin":
        xp = enemy_level * math.ceil(random.randint(1, 3))
        character_statistics["XP"] += xp
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "ogre":
        xp = enemy_level * math.ceil(random.randint(2, 5))
        character_statistics["XP"] += xp
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "orc":
        xp = enemy_level * math.ceil(random.randint(4, 7))
        character_statistics["XP"] += xp
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "wizard":
        xp = enemy_level * math.ceil(random.randint(5, 8))
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "bandit":
        xp = enemy_level * math.ceil(random.randint(3, 5))
        print(f"""Gained {xp} XP""")
    elif combat_opponent.lower() == "dragon":
        xp = enemy_level * math.ceil(random.randint(12, 18))
        print(f"""Gained {xp} XP""")
    else:
        return

    # Set enemy stats
def trigger_battle(combat_opponent, enemy_level):
    # Ensure Enemy isn't too powerful or too weak
    enemy_level = random.randint(1, 1000)
    for i in range(20):
        new_level = random.randint(1, 1000)
        if enemy_level > new_level:
            enemy_level = new_level

    if enemy_level == 0:
        enemy_level = random.randint(.75 * character_statistics["Level"]), math.ceil(1.5 * character_statistics["Level"])
    if enemy_level > math.ceil(1.5 * character_statistics["Level"]):
        enemy_level = math.ceil(1.5 * character_statistics["Level"])
    if enemy_level < math.ceil(.75 * character_statistics["Level"]):
        enemy_level = math.ceil(.75 * character_statistics["Level"])

    # Hydra Battle
    if combat_opponent.lower() == "hydra":
        print(f"""You are in combat against a level {enemy_level} hydra.""")
        enemy_stats["HP"] = 100 * enemy_level
        enemy_stats["Strength"] = 5 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 0

    # Goblin Battle
    elif combat_opponent.lower() == "goblin":
        print(f"""You are in combat against a level {enemy_level} goblin.""")
        enemy_stats["HP"] =  30 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Ogre Battle
    elif combat_opponent.lower() == "ogre":
        print(f"""You are in combat against a level {enemy_level} ogre.""")
        enemy_stats["HP"] =  60 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Orc Battle
    elif combat_opponent.lower() == "orc":
        print(f"""You are in combat against a level {enemy_level} orc.""")
        enemy_stats["HP"] =  80 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Wizard Battle
        print(f"""You are in combat against a level {enemy_level} wizard.""")
        enemy_stats["HP"] =  50 * enemy_level
        enemy_stats["Strength"] = 0
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 3 * enemy_level
        enemy_stats["Magic"] = 4 * enemy_level

    # Golem Battle
        print(f"""You are in combat against a level {enemy_level} golem.""")
        enemy_stats["HP"] =  110 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Bandit Battle
    elif combat_opponent.lower() == "bandit":

        print(f"""You are in combat against a level {enemy_level} bandit.""")
        enemy_stats["HP"] =  40 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 2 * enemy_level
        enemy_stats["Speed"] = 6 * enemy_level
        enemy_stats["Magic"] = 0

    # Dragon Battle
    elif combat_opponent.lower() == "dragon":
        print(f"""You are in combat against a level {enemy_level} dragon.""")
        enemy_stats["HP"] =  150 * enemy_level
        enemy_stats["Strength"] = 6 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 5 * enemy_level

    elif combat_opponent.lower() == "troll":
    # Troll Battle
        print(f"""You are in combat against a level {enemy_level} troll.""")
        enemy_stats["HP"] =  60 * enemy_level
        enemy_stats["Strength"] = 8 * enemy_level
        enemy_stats["Defense"] = 4 * enemy_level
        enemy_stats["Speed"] = 2 * enemy_level
        enemy_stats["Magic"] = 0

    else:
        print("ERROR: No valid enemy selected")
        exit()
    combat_attack()
    enemy_dead(combat_opponent, enemy_level)
    return

    
def combat_attack():


    while enemy_stats["HP"] > 0:
    
        if(random.randint(1, 100) < 90):
            while True:
                choice_attack = input("""You manage to get a jump on the opponent, what do you do?
            
1. Use a weapon
2. Use a spell                                      
3. Use an item
4. Attempt to flee
5. Inventory
6. Stats
7. Enemy Stats
>""")
                print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                try:
                    choice_attack = int(choice_attack)
                except ValueError:
                    print("Please type a number between 1 and 6")
                    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                    continue
                if int(choice_attack) == 1:
                    weapon_stats1 = weapons.get(player_weapons[0])
                    weapon_stats2 = weapons.get(player_weapons[1])
                    weapon_stats3 = weapons.get(player_weapons[2])
                    if "none" not in weapon_stats1["special_power"]:
                        special1 = weapon_stats1["special_power"]
                    else:
                        special1 = ""
                    if "none" not in weapon_stats2["special_power"]:
                        special2 = weapon_stats2["special_power"]
                    else:
                        special2 = ""
                    if "none" not in weapon_stats3["special_power"]:
                        special3 = weapon_stats3["special_power"]
                    else:
                        special3 = ""
                    choice_weapon = input(f"""Which weapon shall you use to strike?
                    
1. {player_weapons[0]}: {weapon_stats1["damage"]} Strenth, {weapon_stats1["hit_chance"]} Hit Chance, {special1}
2. {player_weapons[1]}: {weapon_stats2["damage"]} Strenth, {weapon_stats2["hit_chance"]} Hit Chance, {special2}
3. {player_weapons[2]}: {weapon_stats3["damage"]} Strenth, {weapon_stats3["hit_chance"]} Hit Chance, {special3}
4. Back
>""")
                    print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                    try:
                        choice_weapon = int(choice_weapon)
                    except ValueError:
                        print("Please type a number between 1 and 4")
                        continue
                
                    if int(choice_weapon) == 1:
                        is_valid_weapon(player_weapons[0])
                        break
                    elif int(choice_weapon) == 2:
                        is_valid_weapon(player_weapons[1])
                        break
                    elif int(choice_weapon) == 3:
                        is_valid_weapon(player_weapons[2])
                        break
                    elif int (choice_weapon) == 4:
                        continue  # Goes back to the start of the while loop
                    else: 
                        print("""Please choose a number between 1 and 4""")
                        continue

                elif int(choice_attack) == 2:
                    print("Which Spell would you like to use?\n")
                    print("1. Back")
                    item_lookup = {}
                    print_number = 2

                    for spell, amount in current_spells.items():
                        if amount > 0:
                            print(f"{print_number}. {spell}")
                            item_lookup[print_number] = spell
                            print_number += 1

                    choice_spell = input()
                    try:
                        choice_spell = int(choice_spell)
                    except ValueError:
                        print("Please type a number from the menu.")
                        continue
                    
                    if choice_spell == 1:
                        continue
                    else:
                        is_valid_spell(item_lookup[choice_spell])
                        break
                elif int(choice_attack) == 3:
                    print("Which item would you like to use?\n")
                    print("1. Back")
                    item_lookup = {}
                    print_number = 2

                    for item, amount in inventory.items():
                        if amount > 0:
                            print(f"{print_number}. {item}")
                            item_lookup[print_number] = item
                            print_number += 1

                    choice_item = input()
                    try:
                        choice_item = int(choice_item)
                    except ValueError:
                        print("Please type a number from the menu.")
                        continue
                    
                    if choice_item == 1:
                        continue
                    else:
                        is_valid_item(choice_item, item_lookup)
                        break
                elif int(choice_attack) == 4:
                    print("""You attempted to flee.""")
                    if random.randint(1, 85) < ((character_statistics["Speed"] * 5) - enemy_stats["Speed"] * 2):
                        print("""You successfully escaped the fight!""")
                        return
                    else:
                        print("""You tried to run away, but weren't quick enough. You were hit in the back.
                        
    Lost 5 HP!""")
                        character_statistics["HP"] -= 5
                        if enemy_stats["Strength"] >= enemy_stats["Magic"]:
                            combat_defense("melee")
                        elif enemy_stats["Strength"] < enemy_stats["Magic"]:
                            combat_defense("magic")
                        else:
                            combat_defense("melee")

                elif int(choice_attack) == 5:
                    check_inventory()
                    continue

                elif int(choice_attack) == 6:
                    print_stats()
                    continue

                elif int(choice_attack) == 7:
                    print_enemy_stats()
                    continue

                else:
                    print("""Please enter a number between 1 and 6""")
                    continue
        else:
            if enemy_stats["Strength"] >= enemy_stats["Magic"]:
                combat_defense("melee")
            elif enemy_stats["Strength"] < enemy_stats["Magic"]:
                combat_defense("magic")
            else:
                combat_defense("melee")
    return

def combat_defense(attack_type):

    while enemy_stats["HP"] > 0:

        choice_defense = input("""The opponent manages to get a jump on you, how do you protect yourself?
            
1. Block
2. Dodge
3. Attempt to flee
4. Check Inventory
5. Check Stats
6. Check Enemy Stats
>""")
        print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")


        if int(choice_defense) == 1:
            damage = calculate_player_damage(True, attack_type)
            if damage >= character_statistics["HP"]:
                print("""You are stricken by the enemy, and despite your blocking attempts, your vision begins to fade.
You are slain.""")
                sys.exit()
            elif damage >= 1:
                print(f"""You manage to successfully block, but still suffer some damage.
                
Took {damage} damage! You have {character_statistics["HP"]} HP left.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                combat_attack()

            elif damage <= 0:
                print("""You block the enemy's attacks, and suffer no damage.""")
                combat_attack()

        elif int(choice_defense) == 2:
            if random.randint(1, 100) < (character_statistics["Speed"] * 10) - (enemy_stats["Speed"]):
                print("""You dive out of the way of the oncoming attack, and just manage to dodge without being hurt!""")
                combat_attack()
            else:
                damage = calculate_player_damage(False, attack_type)
                print(f"""You attempt to dodge an oncoming attack, but were unable to get out of the way in time. You suffer some damage.
                      
Took {damage} damage! You have {character_statistics["HP"]} HP remaining.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                combat_attack()

        elif int(choice_defense) == 3:
            print("""You attempted to flee.""")
            if random.randint(1, 100) < ((character_statistics["Speed"] * 5) - (enemy_stats["Speed"] * 2)):
                print("""You successfully escaped the fight!""")
                return
            else:
                damage = calculate_player_damage(False, attack_type)
                print(f"""You tried to run away, but weren't quick enough. The enemy hits you in the back.
                      
Took {damage} damage! You have {character_statistics["HP"]} HP remaining.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
                combat_defense(attack_type)

        elif int(choice_defense) == 4:
            check_inventory()
            continue

        elif int(choice_defense) == 5:
            print_stats()
            continue

        elif int(choice_defense) == 6:
            print_enemy_stats()
            continue

        else:
            print("""Please enter a number between 1 and 6""")
            continue

    return

def calculate_player_damage(is_blocking, attack_type):
    # Enemy attacks with melee
    if is_hit(100 - 10*character_statistics["Speed"]) == False:
        print("""The enemy attack missed!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
        return
    if attack_type.lower() == "melee":
        if is_blocking == True:
            damage_dealt = enemy_stats["Strength"] - math.ceil(2 * character_statistics["Defense"])
            if damage_dealt <= 0:
                damage_dealt = 1
        elif is_blocking == False:
            damage_dealt = enemy_stats["Strength"] - math.ceil(character_statistics["Defense"])
            if damage_dealt <= 0:
                damage_dealt = 1

    # Enemy attacks with magic
    if attack_type.lower() == "magic":
        if is_blocking == True:
            damage_dealt = enemy_stats["Magic"] - math.ceil(2 * character_statistics["Magic"])
            if damage_dealt <= 0:
                damage_dealt = 1
        elif is_blocking == False:
            damage_dealt = enemy_stats["Magic"] - math.ceil(character_statistics["Magic"])
            if damage_dealt <= 0:
                damage_dealt = 1            
    
    if damage_dealt <= 0:
        damage_dealt = 1

    character_statistics["HP"] -= damage_dealt
    does_game_end()
    return damage_dealt

import random

def show_weapon(name, stats):
    print(f"""Weapon Get!
{name} | {stats['rarity']}
{stats['damage']} Damage
{stats['hit_chance']} Hit chance
{stats['type']} Weapon
""")

def weapon_get():
    # Get weapon names and their drop rates
    weapon_names = list(weapons.keys())
    drop_rates = [weapons[w]["drop_rate"] for w in weapon_names]

    # Randomly choose a weapon based on weighted drop chance
    weapon_name = random.choices(weapon_names, weights=drop_rates, k=1)[0]
    stats = weapons[weapon_name]

    # If player has empty slots, auto-assign
    if "Fist" in player_weapons:
        slot = player_weapons.index("Fist")
        player_weapons[slot] = weapon_name
        show_weapon(weapon_name, stats)
        return

    # Otherwise, ask the player if they want to replace something
    show_weapon(weapon_name, stats)
    take_or_leave = input(f"""You found a {weapon_name}, a {stats['rarity']} weapon!
1. Take
2. Leave
""")

    if take_or_leave == "1":
        # Show weapons to replace
        for i, w in enumerate(player_weapons, 1):
            print(f"{i}. {w}")
        leave_weapon = input("Which weapon would you like to leave behind?: ")

        if leave_weapon in {"1", "2", "3"}:
            idx = int(leave_weapon) - 1
            print(f"You chose to leave your {player_weapons[idx]} behind.")
            player_weapons[idx] = weapon_name
        else:
            print("Invalid choice, weapon left behind.")
    else:
        print("You left the weapon behind.")

        
#Template for building events
def trigger_event_0():
    repeat = True

    while repeat == True:
        print("""
1. 
2. 
3. 
4. Stats
5. Inventory 
""")
        
        choice_event0 = input()
        
        if int(choice_event0) == 1:
            print()

        elif int(choice_event0) == 2:
            print()

        elif int(choice_event0) == 3:
            print()
        
        elif int(choice_event0) == 4:
            print_stats()
            repeat = True

        elif int(choice_event0) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# All Game Events

def trigger_pirate_attack():

    repeat = True

    while repeat == True:
        
        if chosen_class == 1 or chosen_class == 3:
            print("""
You engage in combat with the pirates!
1. Attempt to board and steal pirate boat
2. Fire a cannon at the enemy boat
3. Jump into the water for safety
4. Stats
5. Inventory
""")
            choice_event_pirates = input()

            if int(choice_event_pirates) == 1:
                print("""You manage to lose the pirates for a short time, and sneak onto the boat, catching them completely
by surprise. Because of your physical might, they don't stand a chance. The pirates are either
slain or flee into the ocean to escape you. You continue your journey.
                    
Gained 20 XP!""")
                character_statistics["XP"] += 20
                return
            if int(choice_event_pirates) == 2:
                print("""You have no cannon. The pirates do have a cannon. They shoot you.
                    
You are slain.""")
                character_statistics["HP"] = 0
                return
            if choice_event_pirates == 3:
                if character_statistics["Swim"] > 10:
                    print("""You manage to jump into the water and hold your breath long enough while swimming away to lose the pirates.
When you resurface, you find yourself somewhere completely new...""")
                    teleport_random_biome()
                    return
                else:
                    fate = random.randint(1, 3)
                    if fate == 1:
                        print("""You are unable to swim well enough to save yourself from the pirates, but are caught up in a
current and dragged hopelessly to safety. You are quite the lucky hero!""")
                        teleport_random_biome()
                        return

                    if fate == 2:
                        print("""It appears you have forgotten that you cannot swim very well, and swimming for miles is exhausting.
You drown in the water.""")
                        character_statistics["HP"] = 0
                        return
                    if fate == 3:
                        print("""You attempt to swim from the boat, but are far too slow to escape the pirates.
You are captured.""")
                        return
                    
            if choice_event_pirates == 4:
                print_stats()
                repeat = True

            elif int(choice_event_pirates) == 5:
                check_inventory()
                repeat = True

            else:
                print("""Please type a number between 1 and 5.""")
                repeat = True

                
        if chosen_class == 2:
            print("""
You engage in combat with the pirates!
1. Attempt to board and steal pirate boat
2. Conjure a magical storm to destroy the pirates
3. Jump into the water for safety
4. Stats
5. Inventory
""")
            choice_event_pirates = input()
            if int(choice_event_pirates) == 1 and character_statistics["Strength"] >= 10:
                print("""You manage to lose the pirates for a short time, and sneak onto the boat, catching them completely
by surprise. Because of your physical might, they don't stand a chance. The pirates are either
slain or flee into the ocean to escape you. You continue on your journey.
                    
Gained 20 XP!""")
                character_statistics["XP"] += 20
                return
            elif int(choice_event_pirates) == 1 and character_statistics["Strength"] < 10:
                fate = random.randint(1, 2)
                if fate == 1:
                    if character_statistics["Magic"] >= 10:
                        print("""You board the boat, mindlessly firing fireballs in all directions. You manage to scare the pirates off, and take
control of the ship.
                            
Gained 20 XP""")
                        character_statistics["XP"] += 20
                        return
                    else:
                        print("""You were not powerful enough to fight the pirates with your magical abilities, and you were
slain. Rest in peace, great mage.""")
                        character_statistics["HP"] = 0
                        return
                if fate == 2:
                    print("""You foolishly attempt to attack the pirates using a sword, but you were not proficient enough.
You are slain by the pirates.""")
                    character_statistics["HP"] = 0
                    return
            
            if int(choice_event_pirates) == 2:
                if character_statistics["Magic"] > 5 and "Lightning Bolt" in inventory:
                    print("""You conjure up an incredible storm using the power of the lightning bolt obtained from the wizard earlier.
You destroy the pirates, they won't be trying that again for a long time.
                        
Gained 20 XP""")
                    character_statistics["XP"] += 20
                    return
                elif character_statistics["Magic"] > 5 and "Lightning Bolt" not in inventory:
                    print("""You conjure up a storm using your learned magical powers. The pirates retreat, but are not defeated.
                        
Gained 5 XP""")
                    character_statistics["XP"] += 5
                    return
                else:
                    print("""You must not have paid attention in wizarding school. You accidentally create an earthquake underneath
yourself and are slain. Game over, great mage.""")
                    character_statistics["HP"] = 0
                    return
            if int(choice_event_pirates) == 3:
                    if character_statistics["Swim"] > 10:
                        print("""You manage to jump into the water and hold your breath long enough while swimming away to lose the pirates.
When you resurface, you find yourself somewhere completely new...""")
                        teleport_random_biome()
                        return
                    else:
                        fate = random.randint(1, 3)
                        if fate == 1:
                            print("""You are unable to swim well enough to save yourself from the pirates, but are caught up in a
current and dragged hopelessly to safety. You are quite the lucky hero!""")
                            teleport_random_biome()
                            return
                        if fate == 2:
                            print("""It appears you have forgotten that you cannot swim very well, and swimming for miles is exhausting.
You drown in the water.""")
                            character_statistics["HP"] = 0
                            return
                        if fate == 3:
                            print("""You attempt to swim from the boat, but are far too slow to escape the pirates.
You are captured.""")
                            trigger_escape()
                            return
            elif int(choice_event_pirates) == 4:
                print_stats()
                repeat = True

            elif int(choice_event_pirates) == 5:
                check_inventory()
                repeat = True

            else:
                print("""Please type a number between 1 and 5.""")
                repeat = True

def trigger_escape():
    repeat = True

    while repeat == True:
        print("""You awake, tied up in the dark. You have been captured, and need to find a way to escape. What do you do?
1. Attempt to loosen the bands
2. Call out for help
3. Create magical light
4. Stats
5. Inventory 
""")
        
    choice_escape = input()
    attempt = 1
        
    if int(choice_escape) == 1:
        if attempt == 1:
            print("""You wiggle around for a bit, but the bands don't seem to be budging.""")
            attempt += 1
            repeat = True
        if attempt == 2:
            print("""You keep attempting to wiggle away from the bands, but still no dice. You do seem to be making progress, however...""")
            attempt += 1
            repeat = True
        if attempt == 3:
            print("""After a few more moments of struggle, you actually manage to shake the bands off your wrists. What's next?""")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_escape2()

    elif int(choice_escape) == 2:
        print("""You shout for help, but all you can hear in response is your own echo.""")
        repeat = True

    elif int(choice_escape) == 3:
        if character_statistics["Magic"] > 3:
            print("""You struggle for a moment with the bands, but manage to create some light. There isn't much to take in, but you can tell you're in a prison cell.
                  
            Gained 2 Magic
            Lost 5 Energy""")
            character_statistics["Magic"] += 2
            character_statistics["Energy"] -= 5
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_escape3()
        else:
            print("""You simply exhaust yourself trying to create magic. Who really believes in that stuff anyway?
                  
            Lost 10 Energy""")
            character_statistics["Energy"] -= 10
        
    elif int(choice_escape) == 4:
        print_stats()
        repeat = True
    elif int(choice_escape) == 5:
        check_inventory()
        repeat = True

    else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

def trigger_escape2():
    repeat = True

    while repeat == True:
        print("""It's still pitch black, but at least you aren't shackled anymore. What is your escape plan?
1. Blast through the door
2. Sneak out
3. Examine your surroundings
4. Stats
5. Inventory 
""")
        
        choice_escape2 = input()
        
        if int(choice_escape2) == 1:
            if character_statistics["Magic"] >= 5:
                if random.randint(1, 100) < 40:
                    print("""You burst through the door with a fireball, and rush out. Lucky for you, you broke out at night, and despite your
very loud exit, nobody wakes up. You simply walk away, safe... for now.""")
                else:
                    print("""You bust out, and there are at least a million pirates guarding the door. You don't have much time, what do you do?
1. Fight!
2. Run!
3. Surrender!
""")
                    
                    # Import Timer Someday

                    choice_escape2_1 = input()
                    if choice_escape2_1 == 1:
                        damage_taken = random.randint(2, 10)
                        print(f"""You fight through waves of pirates, and feel pretty cool doing so. You manage to get away from them and escape,
But you notice a little late that you had been hurt...
                              
Lost {damage_taken} HP
Gained 15 XP""")
                        character_statistics["HP"] -= damage_taken
                        character_statistics["XP"] += 15

                    elif choice_escape2_1 == 2:
                        if character_statistics["Speed"] >= 5:
                            if random.randint(1, 100) < 70:
                                print("""You run for your life, and don't stop until you stop hearing the footsteps following you. You turn around.
You are safe... for now.
                                      
Gained 5 XP
Gained 1 Speed""")
                                character_statistics["XP"] += 5
                                character_statistics["Speed"] += 1
                                teleport_random_biome()
                                return

                            elif random.randint(1, 100) < 85:
                                HP_lost = 10
                                if HP_lost >= character_statistics["HP"]:
                                    HP_lost = abs(1 - character_statistics["HP"])

                                print(f"""You run and run, but suffer a few arrows in the back while attempting to escape. You survive, but don't feel
so good...
                                      
Lost {HP_lost} HP
Gained 1 Speed""")
                                character_statistics["HP"] -= HP_lost
                                character_statistics["Speed"] += 1
                                teleport_random_biome()
                                return

                            else:
                                print("""You try to run, but are immediately caught. The pirates are not merciful enough to put you back in your cell...
You are slain.""")
                                character_statistics["HP"] = 0
                                return

                        else:
                            if random.randint(1, 100) < 30:
                                print("""Despite your unfit physique, you still manage to outrun the equally out-of-shape pirates. You escape, and
even lose some weight!

Gained 1 Speed
Lost 20 Energy""")
                                character_statistics["Speed"] += 1
                                character_statistics["Energy"] -= 20
                                teleport_random_biome()
                                return
                            
                            elif random.randint(1, 100) < 80:
                                print("""You run, and the pirates manage to get hands on you. You shove them off and keep running, managing to escape,
but take some damage.
                                      
Lost 5 HP
Lost 25 Energy""")
                                character_statistics["HP"] -= 5
                                character_statistics["Energy"] -= 25
                                teleport_random_biome()
                                return
                            
                            else:
                                print("""You definitely aren't in shape. You try running, but run out of energy and the pirates get you. They aren't particularly merciful...
                                      
You are slain.""")
                                character_statistics["HP"] = 0
                                teleport_random_biome()
                                return

                    elif choice_escape2_1 == 3:
                        print("""You get locked up by the pirates again. Deep in the dungeon, no food or water. There is no escape now. 
Your journey ends here.""")
                        character_statistics["HP"] = 0
                        return

            elif character_statistics["Strength"] >= 5 or character_statistics["Defense"] >= 5:
                if random.randint(1, 100) < 40:
                    print("""You smash the door into tiny pieces with your fists and look around, expecting a fight. Apparently you broke out while the pirates
were on break. You simply walk away, safe... for now.""")
                    teleport_random_biome()
                    return
                else:
                    print("""You bust out, and are confronted by numerous guards. Time is running low, you need to choose what to do, quick!
1. Fight!
2. Run!
3. Surrender!
""")
                    
                    # Import Timer Someday
                    choice_escape2_1 = input()
                    if choice_escape2_1 == 1:
                        damage_taken = random.randint(2, 10)
                        print(f"""You fight through waves of pirates, and feel pretty cool doing so. You manage to get away from them and escape,
But you notice a little late that you had been hurt...
                              
Lost {damage_taken} HP
Gained 15 XP""")
                        character_statistics["HP"] -= damage_taken
                        character_statistics["XP"] += 15

                    elif choice_escape2_1 == 2:
                        if character_statistics["Speed"] >= 5:
                            if random.randint(1, 100) < 70:
                                print("""You run for your life, and don't stop until you stop hearing the footsteps following you. You turn around.
You are safe... for now.
                                      
Gained 5 XP
Gained 1 Speed""")
                                character_statistics["XP"] += 5
                                character_statistics["Speed"] += 1
                                teleport_random_biome()
                                return

                            elif random.randint(1, 100) < 85:
                                HP_lost = 10
                                if HP_lost >= character_statistics["HP"]:
                                    HP_lost = abs(1 - character_statistics["HP"])

                                print(f"""You run and run, but suffer a few arrows in the back while attempting to escape. You survive, but don't feel
so good...
                                      
Lost {HP_lost} HP
Gained 1 Speed""")
                                character_statistics["HP"] -= HP_lost
                                character_statistics["Speed"] += 1
                                teleport_random_biome()
                                return

                            else:
                                print("""You try to run, but are immediately caught. The pirates are not merciful enough to put you back in your cell...
You are slain.""")
                                character_statistics["HP"] = 0
                                return

                        else:
                            if random.randint(1, 100) < 30:
                                print("""Despite your unfit physique, you still manage to outrun the equally out-of-shape pirates. You escape, and
even lose some weight!

Gained 1 Speed
Lost 20 Energy""")
                                character_statistics["Speed"] += 1
                                character_statistics["Energy"] -= 20
                                teleport_random_biome()
                                return
                            
                            elif random.randint(1, 100) < 80:
                                print("""You run, and the pirates manage to get hands on you. You shove them off and keep running, managing to escape,
but take some damage.
                                      
Lost 5 HP
Lost 25 Energy""")
                                character_statistics["HP"] -= 5
                                character_statistics["Energy"] -= 25
                                teleport_random_biome()
                                return
                            
                            else:
                                print("""You definitely aren't in shape. You try running, but run out of energy and the pirates get you. They aren't particularly merciful...
                                      
You are slain.""")
                                character_statistics["HP"] = 0
                                teleport_random_biome()
                                return

                    elif choice_escape2_1 == 3:
                        print("""You get locked up by the pirates again. Deep in the dungeon, no food or water. There is no escape now. 
Your journey ends here.""")
                        character_statistics["HP"] = 0
                        return

        elif int(choice_escape2) == 2:
            if room_checked == True:
                print("""You quietly open the door. The pirates must be on break, nobody is around... 
You leave safely... For now.
""")
                teleport_random_biome()
                return
            else:
                if random.randint(1, 100) < 40:
                    print("""You quietly open the door. The pirates must be on break, nobody is around... 
    You leave safely... For now.
""")
                    teleport_random_biome()
                    return
                
                elif random.randint(1, 100) < 85:
                    print("""You try sneaking out, but end up getting seen just as you're about to escape. You manage to run to safety, but
    lost a significant amount of energy.
                        
    Lost 50 Energy""")
                    
                    character_statistics["Energy"] -= 50
                    teleport_random_biome()
                    return
                
                else:
                    print("""You sneak around the prison grounds, thinking you're very sneaky and quiet. Apparently you weren't. The pirates have
    you surrounded, and eventually you are recaptured. The pirates are not so merciful with you.
    You are slain.""")
                    character_statistics["HP"] = 0
                    return

        elif int(choice_escape2) == 3:
            if random.randint(1, 100) < 20:
                print("""It is certainly a dreary living space. There are a few sticks and stones lying about the cold stone floor, with a wooden
door and no windows. Upon closer inspection, you realize that the door might not even be locked...""")
                room_checked = True
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_escape2()
            elif random.randint(1, 100) < 40:
                print("""There is no bed.""")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_escape2()
            elif random.randint(1, 100) < 60:
                print("""There are a few torches, unfortunately they have long since burnt out.""")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_escape2()
            elif random.randint(1, 100) < 80:
                if inventory["Wood"] < 2:
                    print("""You decide to grab yourself a piece of wood off the floor, perhaps it will come in handy later.""")
                    inventory["Wood"] += 1
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    trigger_escape2()
                else:
                    print("""There are a few pieces of wood and some pebbles laying around on the floor.""")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    trigger_escape2()
            else:
                print("""This certainly isn't a pretty place...""")
        
        elif int(choice_escape2) == 4:
            print_stats()
            repeat = True

        elif int(choice_escape2) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

def trigger_escape3():
    repeat = True

    while repeat == True:
        print("""Now that you have a better idea of what's going on, you need to think of a way to escape. You slip out of your restraints, and in the room you see
a door, a boarded window, a bucket, a few pebbles and a stick. How do you escape?
1. Use magic to blast the door down
2. Forge a crowbar from the pebbles and sneak out the window
3. Place the bucket on your head.
4. Stats
5. Inventory 
""")
        
        choice_escape3 = input()
        
        if int(choice_escape3) == 1: 
            if random.randint(1, 100) < character_statistics["Magic"] * 5:
                print("""You manage to blast the door down with a lightning bolt, and the subsequent burst of light stuns the pirates guarding the door.
The pirates scramble to figure out what's going on, and you manage to slip away in the confusion.""")
                teleport_random_biome()
                return
            else:
                damage = character_statistics["Magic"]
                if damage >= character_statistics["HP"]:
                    damage = character_statistics["HP"] - 1
                print("""You attempt to blow the door down, but accidentally summon a fireball too large, blasting the door down and slaying all pirates, but harming yourself
in the process. After blacking out for a while, you awake to find yourself alone. You limp away, safe... for now.
                      
Took {damage} damage!""")
                character_statistics["HP"] -= damage
                teleport_random_biome()
                return

        elif int(choice_escape3) == 2:
            if "Pebbles" not in inventory or inventory["Pebbles"] < 2 and character_statistics["Magic"] < 12:
                print("""You attempt to use the pebbles, but have no way of forging them into anything. Even with your attempts to create a fire to smelt them, there is no way.
You decide to take one with you anyway, just in case.""")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_escape3()
            elif character_statistics["Magic"] >= 12:
                if random.randint(1, 100) < 60:
                    print("""You manage to form the pebbles into a crowbar using your magic. It drains your energy, but you manage to escape by using it to crawl through the
window and sneak away. Unfortunately, you forgot to bring the crowbar with you. Oh well.
                      
Lost 20 Energy""")
                    character_statistics["Energy"] -= 20
                    teleport_random_biome()
                    return
                else:
                    if random.randint(1,100) < character_statistics["Speed"] * 5:
                        print("""You manage to forge a crowbar using magic, but while trying to sneak out, you are seen by the guards and attempt to flee.
You successfully make your getaway, and feel pretty good afterwards!
                              
Gained 1 Speed
Gained 5 Energy""")
                        character_statistics["Speed"] += 1
                        character_statistics["Energy"] += 5
                        teleport_random_biome()
                        return
                    else:
                        print("""You manage to forge a crowbar using magic, but while trying to sneak out, you are seen by the guards and attempt to flee.
Unfortunately, you were too slow and are forced to fight, leaving you badly wounded, but alive. You escape.
                              
Down to 1 HP!""")
                        character_statistics["HP"] = 1
                        teleport_random_biome()
                        return
            else:
                print("""You cannot create a crowbar.""")

        elif int(choice_escape3) == 3:
            if random.randint(1, 100) < 99:
                print("""Well done. Now you cannot see and look like a fool. What did you expect to happen?
                      
Lost 5 Morale""")
                character_statistics["Morale"] -= 5
                return
            else:
                print("""You place the bucket on your head at the exact moment a pirate happens to walk in. He must be blind, because he couldn't see you and left the
door open behind him. You quietly sneak out and nobody bats an eye. How nice!""")
                teleport_random_biome()
                return
        
        elif int(choice_escape3) == 4:
            print_stats()
            repeat = True

        elif int(choice_escape3) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Any Biome
def trigger_shop():
    repeat = True

    while repeat:
        print(f"""You come across a vendor during your travels. 
\"I've got wares, why don't you take a look?\" He suspiciously says.
You've got {inventory['Money']} money
1. Purchase
2. Sell
3. Leave
4. Stats
5. Inventory 
""")
        
        choice_shop = int(input("Choose an option: "))
        
        if choice_shop == 1:  # Purchase
            print("""1. Back
2. Wood (2 Money)
3. Iron (3 Money)""")
            # As player levels up, more shop options appear
            if character_statistics["Level"] > 2:
                print("4. Gold")
            if character_statistics["Level"] > 4:
                print("5. ")

            choice_purchase = int(input("Choose an item: "))

            if choice_purchase == 1:
                continue

            elif choice_purchase == 2:  # Buy wood
                quantity = int(input("How many would you like to purchase? "))
                total_cost = purchase_price["Wood"] * quantity
                if inventory["Money"] >= total_cost:
                    inventory["Money"] -= total_cost
                    inventory["Wood"] += quantity
                    print(f"You bought {quantity} Wood for {total_cost} money!")
                else:
                    print("Not enough money!")

            elif choice_purchase == 3:  # Buy iron
                quantity = int(input("How many would you like to purchase? "))
                total_cost = purchase_price["Iron"] * quantity
                if inventory["Money"] >= total_cost:
                    inventory["Money"] -= total_cost
                    inventory["Iron"] += quantity
                    print(f"You bought {quantity} Iron for {total_cost} money!")
                else:
                    print("Not enough money!")

            # Can buy gold, but only with high enough level.
            elif choice_purchase == 4 and character_statistics["Level"] > 2:
                quantity = int(input("How many would you like to purchase? "))
                total_cost = purchase_price["Gold"] * quantity
                if inventory["Money"] >= total_cost:
                    inventory["Money"] -= total_cost
                    inventory["Gold"] += quantity
                    print(f"You bought {quantity} Gold for {total_cost} money!")
                else:
                    print("Not enough money!")

            else:
                print("""Not a valid item.""")


        elif choice_shop == 2:  # Sell
            print("What would you like to sell?")
            print("1. Back")
            options = {}
            option_number = 2

            for item, qty in inventory.items():
                if item != "Money" and qty > 0:  # can’t sell money
                    print(f"{option_number}. {item} ({qty} available, {sell_price.get(item, 0)} Money)")
                    options[option_number] = item
                    option_number += 1

            choice_sell = int(input("Choose an item: "))
            if choice_sell == 1:
                continue
            elif choice_sell in options:
                item = options[choice_sell]
                quantity = int(input(f"How many {item} do you want to sell? "))
                if inventory[item] >= quantity:
                    earned = sell_price[item] * quantity
                    inventory[item] -= quantity
                    inventory["Money"] += earned
                    print(f"You sold {quantity} {item} for {earned} money!")
                else:
                    print(f"Not enough {item} to sell.")

        elif choice_shop == 3:
            print("\"Not today eh? Maybe next time...\" He creepily says as you walk away.")
            return
        
        elif choice_shop == 4:
            print_stats()

        elif choice_shop == 5:
            check_inventory()

        else:
            print("Please type a number between 1 and 5.")

# Starting Event
def trigger_event1():
    repeat = True

    while repeat == True:
        
        print("""
A challenge stands in front of you: a simple goblin. What will you do fighter?
1. Attack with the sword
2. Strike him with a fireball
3. Run for your pitiful little life
4. Stats
5. Inventory
""")
        choice_event1 = input()

        if int(choice_event1) == 1 and character_statistics["Strength"] >= 5:
            print("""Well done fighter! You have slain the goblin.
                
Gained 10 XP""")
            character_statistics["XP"] += 10
            return

        elif int(choice_event1) == 1 and character_statistics["Defense"] >= 5:
            print("""Well done fighter! You have slain the goblin.
                
Gained 10 XP""")
            character_statistics["XP"] += 10
            return

        elif int(choice_event1) == 1 and character_statistics["Defense"] < 5 and character_statistics["Strength"] < 5:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""You have been smitten fighter! You were not strong enough to fight this goblin with the sword.
                      
Lost 5 HP""")
                character_statistics["HP"] -= 5
                return

            elif fate == 2:
                print("""The goblin has bested you traveller. This is the end of the road for you. Let your name rest in legend.
                      
Lost 20 HP""")
                character_statistics["HP"] -= 20
                return
            
        elif int(choice_event1) == 2 and character_statistics["Magic"] >= 5:
            print("""Well done fighter! You have slain the goblin.
                            
Gained 10 XP""")
            character_statistics["XP"] += 10
            return

        elif int(choice_event1) == 2 and character_statistics["Magic"] < 5:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""You have been smitten fighter! You were not experienced enough to fight the goblin with a fireball.
                      
Lost 5 HP""")
                character_statistics["HP"] -= 5
                return

            elif fate == 2:
                print("""The goblin has bested you traveller. This is the end of the road for you. Let your name rest in legend.
                      
Lost 20 HP""")
                character_statistics["HP"] -= 20
                return
        
        elif int(choice_event1) == 3:
            print("""You have run away like a coward. You are not fit to be a fighter for this kingdom.
We wish you well, traveller. Goodbye.""")
            character_statistics["HP"] -= 20
            return
        
        elif int(choice_event1) == 4:
            print_stats()
            repeat = True

        elif int(choice_event1) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

        
# Swamp Event
def trigger_event2():
    repeat = True

    while repeat == True:
        
        print("""
Another challenge awaits! You find yourself in a thick swamp. What will you do?
1. Scavenge for resources
2. Explore further
3. Rest yourself
4. Stats
5. Inventory
""")
        
        enter_setting("Swamp")

        choice_event2 = input()

        if int(choice_event2) == 1:
            fate = random.randint(1, 3)
            if fate == 1:
                print("""Well done fighter! You have found some wood.
                        
Gained 1 Wood""")
                
                inventory["Wood"] += 1
                setting["Tundra"] = True
                setting["Swamp"] = False
                return
            
            elif fate == 2:
                print("""Well done fighter! You have found some iron.
                        
Gained 1 Iron""")
                
                inventory["Iron"] += 1
                setting["Tundra"] = True
                setting["Swamp"] = False
                return
            
            elif fate == 3:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_battle("goblin")
                return
            
        elif int(choice_event2) == 2:
            print("""You have chosen to explore further.""")
            teleport_random_biome()

            return
        
        elif int(choice_event2) == 3:
            print(f"""You rest for the night. You have returned to full health.
                  
HP returns to {max_HP}.""")

            if character_statistics["HP"] < max_HP:
                character_statistics["HP"] = max_HP

            return
        
        elif int(choice_event2) == 4:
            print_stats()
            repeat = True

        elif int(choice_event2) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Forest Event
def trigger_event3():
    repeat = True

    while repeat == True:
        
        print("""While stumbling across the forest, you are ambushed by a group of gnomes. What will you do?
              
1. Attempt a spin attack with your sword
2. Cast a lightning strike to destroy the ambush
3. Attempt to bribe the gnomes
4. Stats
5. Inventory
""")
        choice_event3 = input()

        if int(choice_event3) == 1 and character_statistics["Strength"] >= 15:
            print("""You spin around, sword outstretched, daring any gnomoes to come close to you.
They run to you in hoardes, but are sliced down and slain by your sword.
                
Gained 20 XP""")
            character_statistics["XP"] += 20
            return

        elif int(choice_event3) == 1 and character_statistics["Strength"] < 15:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""You accidentally throw out your shoulder while spinning. The attacking gnomes feel pity and leave you alone.
                      
Lost 5 HP
Lost 2 Strength""")
                character_statistics["HP"] -= 5
                character_statistics["Strength"] -= 2
                return

            elif fate == 2:
                print("""The sword flies from your hand. The gnomes annihilate you. Let your name rest in legend.
                      
You have died""")
                character_statistics["HP"] -= 99999999
                return
            
        elif int(choice_event3) == 2 and "Lightning Bolt" in inventory:
            print("""As the sound of thunder cracks above, the gnomes freeze. They glance into the sky, only to see
their lives flash before their eyes. After a moment, you are the only nearby creature left standing.
                            
Gained 25 XP""")
            character_statistics["XP"] += 25
            return

        elif int(choice_event3) == 2 and "Lightning Bolt" not in inventory:
            fate = random.randint(1, 3)
            if fate == 1:
                print("""You try reeeeeaaaallly hard to make a lightning bolt come down, but it just doesn't happen.
Wonder how those wizards do it. The gnomes watch your pathetic attempt and realize there is no benefit
to killing you. They leave you alone, but you are very embarrassed.
                      
Lost 15 Morale""")
                character_statistics["Morale"] -= 15
                return

            elif fate == 2:
                print("""You accidentally strike yourself with lightning and paralyze yourself. The gnomes leave you for
dead. However, you manage to survive. Barely.
                      
1 HP Remaining""")
                character_statistics["HP"] = 1
                return
            
            elif fate == 3:
                print("""You failed to cast a lightning bolt, and the gnomes have slain you. May your name rest in legend.
                      
You have died.""")
                character_statistics["HP"] = 0
                return
        
        elif int(choice_event3) == 3 and inventory["Money"] >= 2:
            print("""You have enough money to fulfill the gnome king's demands. He takes 2 coins, but leaves
you with your life.
                  
Lost 2 Money""")
            inventory["Money"] -= 2
            return
        
        elif int(choice_event3) == 3 and inventory["Gold"] >= 1:
            print("""You have enough gold to fulfill the gnome king's demands. He takes 2 coins, but leaves
you with your life.
            
Lost 1 Gold""")
            inventory["Gold"] -= 1
            return

        elif int(choice_event3) == 3 and inventory["Gold"] < 1 and inventory["Money"] < 2:
            print("""Your offering was not good enough for the gnome king, and you were sacrificed to the gnome
Gods. You have been slain. May your name rest in legend.
            
You have died.""")
            character_statistics["HP"] = 0
            return
        
        elif int(choice_event3) == 4:
            print_stats()
            repeat = True

        elif int(choice_event3) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Tundra Event
def trigger_event4():
    repeat = True

    while repeat == True:
        
        print("""
You come across an igloo in the snow covered landscape. You walk inside. What do you do there?
1. Take a nap
2. Melt the igloo to search for more goods
3. Take an icicle bolt spell book from the wall
4. Stats
5. Inventory
""")
        choice_event4 = input()

        if int(choice_event4) == 1:
            print("""You choose to take a nap
                  
Healed 5 HP""")

            character_statistics["HP"] += 5
            if character_statistics["HP"] > 20:
                character_statistics["HP"] = 20

            return
        
        elif int(choice_event4) == 2:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""You find some gold in the melted remains of the poor igloo.
                      
Obtained 2 Gold
Gained 5 XP""")

                character_statistics["XP"] += 5
                inventory["Gold"] +=2
                return
            
            if fate == 2:
                print("""You accidentally manage to melt the entire tundra. You are now in the ocean. You monster.""")
                
                setting["Ocean"] = True
                setting["Tundra"] = False
                return
            
        elif int(choice_event4) == 3:
            print("""You take the book from the shelf. You had to stretch a little to reach it, but you managed
to find a chair, so you were able to reach. You glance through the book. There are multiple different
spells, but only one page is readable. Also you can't really read so you needed an easy book.
                  
Obtained Ice Blast""")
            inventory["Ice Blast"] = 1

        elif int(choice_event4) == 4:
            print_stats()
            repeat = True

        elif int(choice_event4) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Swamp Event
def trigger_event5():
    repeat = True

    while repeat == True:
        
        print("""
As you wander throughout the swamp, confused and lost, you encounter an old witch. She invites you
to come inside and try a potion. What will you do?
1. Drink the potion the witch gives you
2. Slay the witch
3. Run away
4. Stats
5. Inventory
""")
        choice_event5 = input()

        if int(choice_event5) == 1:
            fate = random.randint(1, 10)
            if fate == 1 or fate == 2:
                print("""You drink the potion. It is sweet to the taste. You feel your energy surging!
                      
Speed increased by 10!
Gained 5 XP""")
                character_statistics["Speed"] += 10
                character_statistics["XP"] += 5
                return
            if fate == 3:
                print("""You drink the potion. It tastes bitter, but surprisingly tasty. You feel empowered!
                      
Strength increased by 10!
Gained 5 XP""")
                character_statistics["Strength"] += 10
                character_statistics["XP"] += 5
                return
            if fate == 4:
                print("""You drink the potion. It does not taste good. You don't feel too sick yet though...
                      
Lost 10 Morale""")
                character_statistics["Morale"] -= 10
                return
            if fate == 5:
                print("""You drink the potion. Nothing happens. It was probably just water, but you're polite and leave with a thanks.""")
                return
            if fate == 6:
                print("""You drink the potion. You start feeling very sick, and lose much of your energy to continue fighting.
                      
Energy decreased by 50""")
                character_statistics["Energy"] -= 50
                return
            if fate == 7:
                print("""You drink the potion. Apparently it's just clam chowder. Yum!
                      
Swim increased by 10!""")
                character_statistics["Swim"] += 10
                return
            if fate == 8:
                print("""You drink the potion. It is very obviously poison. You'll learn to walk it off.
                      
Down to 1 HP!""")
                character_statistics["HP"] = 1
                return
            if fate == 9:
                print("""You drink the potion. You can't tell immediately what happens, but you feel great!
                      
Gained 10 HP""")

                character_statistics["HP"] += 10
                if character_statistics["HP"] > 20:
                    character_statistics["HP"] = 20
                    character_statistics["Energy"] += 5
                    if character_statistics["Energy"] > 100:
                        character_statistics["Energy"] = 100
                return
            if fate == 10:
                print("""You drink the potion. It was a love potion. Unfortunately, there are no fair maidens in the kingdom
for quite a ways. You still find yourself walking with a spring in your step!
                      
Gained 10 Morale""")
                character_statistics["Morale"] += 10
                if character_statistics["Morale"] > 100:
                    character_statistics["Morale"] = 10

        elif int(choice_event5) == 2 and character_statistics["Strength"] >= 15:
            print("""You kill the witch. You didn't even give her a chance to explain herself. Maybe the true
monster is you...
                  
Gained 20 XP""")
            character_statistics["XP"] += 20


        elif int(choice_event5) == 2 and character_statistics["Magic"] >= 15:
            print("""You blast the poor witch's head right off her shoulders with a fireball. You didn't even give her a chance to explain herself. 
Maybe the true monster is you...
                  
Gained 20 XP""")
            character_statistics["XP"] += 20

        elif int(choice_event5) == 2 and character_statistics["Strength"] < 15 and character_statistics["Magic"] < 15:
            fate = random.randint(1,2)
            if fate == 1:
                print("""The witch splashes you with poison potions while you stumble around trying to fight her. It hurts very
badly, but maybe you deserve this...
                      
Lost 10 HP""")
                character_statistics["HP"] -= 10
                return

            elif fate == 2 and character_statistics["Speed"] > 5:
                print("""You fail to slay the witch, but luckily are able to escape before more damage can be done.""")
                newsetting = random.randint(1,5)
                setting["Swamp"] = False
                if newsetting == 1:
                    setting["Forest"] = True
                    print("You have arrived in a forest.")
                    return
                if newsetting == 2:
                    setting["Plains"] = True
                    print("You have arrived in a plain.")
                    return
                if newsetting == 3:
                    setting["Tundra"] = True
                    print("You have arrived in a tundra.")
                    return
                if newsetting == 4:
                    setting["Jungle"] = True
                    print("You have arrived in a jungle.")
                    return
                if newsetting == 5:
                    setting["Ocean"] = True
                    print("You have arrived in an ocean.")
                    return

            elif fate == 2 and character_statistics["Defense"] > 10:
                fate_again = random.randint(1,2)
                if fate_again == 1:
                    print("""The witch splashes you with poison potions while you stumble around trying to fight her. It hurts very
badly, but maybe you deserve this...
                      
Lost 2 HP""")
                    character_statistics["HP"] -= 2
                    return
                if fate_again == 2:
                    print("""The witch splashes you with poison potions while you stumble around trying to fight her. It hurts very
badly, but maybe you deserve this...
                      
Lost 5 HP""")
                    character_statistics["HP"] -= 5
                    return

            else:
                if random.randint(1, 100) < 60:
                    print("""You trip and break all your bones. The witch cooks you alive in her boiling pot.
                      
You have died""")
                    character_statistics["HP"] = 0
                    return
                else:
                    print("""While you might not be an athlete, neither, it seems, is the witch. You somehow outrun her, but you're pretty exhausted.
                          
Lost 10 Energy""")
                    character_statistics["Energy"] -= 10
                    return


        elif int(choice_event5) == 3 and character_statistics["Speed"] > 5:
            print("""You manage to escape the witch, and are lucky enough to survive.""")
            newsetting = random.randint(1,5)
            setting["Swamp"] = False
            teleport_random_biome()
            return

        elif int(choice_event5) == 3:
            if random.randint(1, 100) < 75:
                print("""You successfully escape the situation, but remain in the swamp.""")
                return
            else:
                print("""You run away, but you end up stubbing your toe on the way out. Ouch...
                      
Lost 3 HP""")
                character_statistics["HP"] -= 3
                return

        elif int(choice_event5) == 4:
            print_stats()
            repeat = True

        elif int(choice_event5) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Swamp Event
def trigger_event6():
    repeat = True

    while repeat == True:
        
        print("""While sloshing through some mud, you feel something rubbing against your foot. What will you do?
1. Reach down and grab the thing rubbing against you
2. Attempt to clear the mud by digging really fast to get a better look
3. Ignore whatever it was and keep sloshing around
4. Stats
5. Inventory
""")
        choice_event6 = input()
        if int(choice_event6) == 1:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""Turns out it was just some gold. Lucky you!
                      
Obtained 5 Gold""")
                inventory["Gold"] += 5
                return

            if fate == 2:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event6_enemy()
                return
            
        elif int(choice_event6) == 2:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""You manage to find atlantis under the mud. You grab 5 gold and you cover it back up. Not worth your time.
                      
Gained 5 Gold""")
                inventory["Gold"] += 5
                return
            if fate == 2:
                print("""You can't dig fast enough to clear mud. You feel sad.
                      
Lost 5 Morale""")
                character_statistics["Morale"] -= 5
                return

        elif int(choice_event6) == 3:
            print("""You choose to ignore whatever was in the mud and continue on your journey.""")
            return

        elif int(choice_event6) == 4:
            print_stats()
            repeat = True

        elif int(choice_event6) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

def trigger_event6_enemy():
    repeat = True

    while repeat == True:

        print("""
Oh no! It's a shark... Your worst nightmare! How will you rid of this foe?
1. Bite it!
2. Blast it with a fireball
3. Swim as fast as you can
4. Stats
5. Inventory
""")

        choice_event6 = input()
        if int(choice_event6) == 1 and character_statistics["Strength"] >= 10:
            print("""The shark looks at you, confused. 'Why did you bite me?' It seems to wonder. 
Rude. The shark swims away, giving you a stank look while he goes.
                  
Gained 5 XP!
""")
            character_statistics["XP"] += 5
            return

        elif int(choice_event6) == 1 and character_statistics["Defense"] >= 10:
            print("""The shark looks at you, confused. 'Why did you bite me?' It seems to wonder. 
Rude. The shark swims away, giving you a stank look while he goes.
                    
Gained 5 XP!
""")
            character_statistics["XP"] += 5
            return
        
        elif int(choice_event6) == 1 and character_statistics["Strength"] < 10 and character_statistics["Defense"] < 10:
            fate = random.randint(1, 2)
            if fate == 1:
                print("""The shark bites your face and you die. May your name rest in legend.
                      
You have died.""")
                character_statistics["HP"] = 0
                return

            if fate == 2:
                print("""You end up scaring the spooky shark with your menacing bite force, but you swallow lots of mud in the process.
You start feeling a bit sick...
                      
Lost 10 Morale
Lost 10 Energy""")
                character_statistics["Morale"] -= 10
                character_statistics["Energy"] -= 10
                return

        elif int(choice_event6) == 2 and character_statistics["Magic"] > 10:
            print("""You manage to masterfully weave a fireball into the mud and hit the shark somehow...
Well fighter, I am impressed.
                  
Gained 5 XP
Gained 2 Magic""")
            character_statistics["XP"] += 5
            character_statistics["Magic"] += 2
            return

        elif int(choice_event6) == 2 and character_statistics["Magic"] <= 10:
            print("""The fireball blows up in your face upon striking the mud. What were you thinking?
                  
Lost 5 HP""")
            character_statistics["HP"] -= 5
            return

        elif int(choice_event6) == 3 and character_statistics["Swim"] >= 5:
            print("""You swim through the mud and escape the shark. Turns out sharks don't swim well in mud...
                  
You have escaped.""")
            return
        
        elif int(choice_event6) == 3 and character_statistics["Swim"] < 5:
            if inventory["Gold"] > 0:
                print("""The shark slowly swims in circles around you. Luckily for you, it just wants your money.
                    
Lost all gold""")
                inventory["Gold"] = 0
                return
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    print("""The shark only wanted your money, but unfortunately for you, you have no money.
Embarrasing. The shark rolls his eyes and flicks you a coin. Lucky you!
                          
Gained 1 Gold""")
                    inventory["Gold"] += 1
                    return
                if fate == 2:
                    print("""The shark demands payment in exchange for your life. You empty your pockets, but unfortunately
They were already empty. The shark, as promised, takes your life. You are slain.""")
                    character_statistics["HP"] = 0
                    return

        elif int(choice_event6) == 4:
                print_stats()
                repeat = True

        elif int(choice_event6) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Forest Event
def trigger_event7():
    print("""
You encounter a wizard deep in the forest. He appears to be nice! He hands you a book. What a nice guy.
          
Obtain Lightning Bolt""")

    inventory["Lightning Bolt"] = 1

# Plains/Forest/Jungle Event
def trigger_event8():
    repeat = True

    while repeat == True:
        print("""
You come across an ocean. What will you do?
1. Go fishing and relax
2. Turn around and ignore it
3. Build a boat and sail the seas
4. Stats
5. Inventory
""")
        choice_event8 = input()

        if int(choice_event8) == 1:
            fate = random.randint(1, 3)
            if fate == 1:
                print("""You manage to catch a big fish. You eat it, and it makes you happy!
You decide to move on from the ocean.
                      
Gained 10 Morale
Gained 5 HP
""")
                character_statistics["HP"] += 5
                character_statistics["Morale"] += 10
                teleport_random_biome()
                return
            if fate == 2:
                print("""You are unable to catch any fish. You are sad.
You decide to move on from the ocean.
                      
Lost 10 Morale
""")
                character_statistics["Morale"] -= 10
                teleport_random_biome()
                return
            if fate == 3:
                print("""You let your guard down, and you are attacked by a group of pirates.""")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_pirate_attack()
                return

        elif int(choice_event8) == 2:
            print("""You decide to walk away from the ocean. Can't blame you, who knows what's in there...""")

            teleport_random_biome()
            return
        
        elif int(choice_event8) == 3 and character_statistics["Swim"] >= 5:
            is_On_Water = True
            enter_setting("Ocean")
            return

        elif int(choice_event8) == 3 and character_statistics["Swim"] < 5:
            print("""As you build a boat, you realize you don't know how to swim. Probably not the greatest idea to go sailing. You decide to continue on.""")
            teleport_random_biome()
            return
        
        elif int(choice_event8) == 4:
            print_stats()
            repeat = True

        elif int(choice_event8) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True 

# Tundra Event
def trigger_event9():
    repeat = True

    while repeat == True:
        print("""While travelling through the tundra, you come across a large, icy river, filled to the brim
with hungry and violent fish. What will you do?
              
1. Attempt to slay the fish for food
2. Run through the icy river
3. Build a bridge to cross the river
4. Stats
5. Inventory 
""")
        choice_event9 = input()
        if int(choice_event9) == 1:
            if character_statistics["Strength"] > 7 or character_statistics["Defense"] > 7:
                print("""You successfully obtain some food.
                      
                Energy Fully Restored!""")
                character_statistics["Energy"] = 100
                return
            else:
                print("""Turns out it's pretty hard to fish with your hands, particularly when the fish have very sharp teeth.
You're bit once and choose to give up.
                      
Lost 2 HP
Lost 10 Morale
""")
                character_statistics["HP"] -= 2
                character_statistics["Morale"] -= 10
                return
        elif int(choice_event9) == 2 and character_statistics["Swim"] > 2:
            fate = random.randint(1, 3)
            if fate == 1:
                HP_Loss = random.randint(2, 10)
                print(f"""You attempted to run through the river, but it was deeper than expected. You swam quickly enough to escape, but were hurt in the process.
                      
                Lost {HP_Loss} HP
                Lost 15 Energy""")
                character_statistics["HP"] -= HP_Loss
                character_statistics["Energy"] -= 15
                return
            if fate == 2:
                print("""You manage to run through the river, and while you suffered from the cold, you were not badly hurt.
                      
Lost 1 HP
Lost 5 Energy""")
                character_statistics["HP"] -= 1
                character_statistics["Energy"] -= 5
                return
            if fate == 3:
                if character_statistics["Speed"] > 5:
                    print("""Luckily for you, the river was just shallow enough for you to run without any fish biting you.
                          
Gained 1 Speed""")
                    character_statistics["Speed"] += 1
                    return
                else:
                    print("""You attempt to run across the river, but trip and are eaten by the fish. You are slain.""")
                    character_statistics["HP"] = 0
                    return
        elif int(choice_event9) == 2 and character_statistics["Swim"] <= 2:
            fate = random.randint(1, 3)
            if fate == 1:
                print("""You cannot swim, and the river was a little bit too deep. You are unable to escape the fish and are eaten.
You are slain.""")
                character_statistics["HP"] = 0
                return
            if fate == 2:
                HP_Loss = random.randint(5, 15)
                if character_statistics["HP"] - HP_Loss < 1:
                    print(f"""You were lucky, and the river was just shallow enough for you to get across, suffering only a few
fish bites. You survive.
                          
You are left with 1 HP.""")
                    character_statistics["HP"] = 1
                    return
                else:
                    print(f"""You were lucky, and the river was just shallow enough for you to get across, suffering only a few
fish bites. You survive.
                        
You lost {HP_Loss} HP""")
                    character_statistics["HP"] -= HP_Loss
                    return
            if fate == 3:
                print("""You somehow manage to escape over the river unscathed, you must be a track star or something.
                      
Gained 1 Swimming!""")
                character_statistics["Swim"] += 1
                return
        elif int(choice_event9) == 3:
            if inventory["Wood"] > 1:
                print("""You successfully build a bridge, and use it to cross the river safely.
                      
                Lost 2 Wood""")
                inventory["Wood"] -= 2
                return
            elif inventory["Wood"] <= 1:
                print("""You have nothing to build a bridge with. Not sure what you were expecting to build.
You obviously do not succeed at building a bridge, and were forced to attempt crossing on your own.
You cross safely, but are badly hurt and tired.
                      
Down to 1 HP!
Down to 1 Energy!""")
                character_statistics["HP"] = 1
                character_statistics["Energy"] = 1
                return
            
        elif int(choice_event9) == 4:
            print_stats()
            repeat = True

        elif int(choice_event9) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Plains Event
def trigger_event10():
    repeat = True

    while repeat == True:
        print("""You discover the fountain of youth while wandering through the plains. What do you do?
1. Enter the fountain
2. Have a refreshing drink
3. Store some for later
4. Stats
5. Inventory 
""")
        choice_event10 = input()

        if int(choice_event10) == 1:
            fate = random.randint(1, 2)
            if fate == 1:
                if character_statistics["HP"] - 5 <= 0:
                    HP_lost = abs(1 - character_statistics["HP"])
                    if HP_lost == 0:
                        print("""Overzealous, you choose to dive into the fountain head first, consequently striking your head on the bottom of the fountain.
You are knocked unconscious, and are unable to recover. You drown""")
                        character_statistics["HP"] = 0
                        break
                    else:
                        character_statistics["HP"] = 1

                elif character_statistics["HP"] - 5 > 0:
                    HP_lost = 5
                    character_statistics["HP"] -= 5

                print(f"""Overzealous, you choose to dive into the fountain head first, consequently striking your head on the bottom of the fountain.
You are knocked unconscious, but are able to recover before drowning. It definitely hurt, though.
                    
lost {HP_lost} HP!""")

        elif int(choice_event10) == 2:
            fate = random.randint(1, 3)
            if fate == 1:
                print("""After taking a few sips, you notice some odd floaties in the water. You feel really uncomfortable. But you feel surprisingly good...
                    
Permanent HP increase!
Gained Full HP
""")
                max_HP += 2
                character_statistics["HP"] += 100
                break
            if fate == 2:
                print("""You take a few sips, but start to feel really sick. You notice some odd floaties in the water. You feel uncomfortable...
                      
Permanent HP decrease
""")
                max_HP -= 2
                break
            if fate == 3:
                print("""After a refreshing drink, you turn away from the water.""")
                break


        elif int(choice_event10) == 3:
            print('''A small head emerges from the deep, "That ain\'t yours you little punk." says the strange creature.''')
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10_1()

        elif int(choice_event10) == 4:
            print_stats()
            repeat = True

        elif int(choice_event10) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Side Event
def trigger_event10_1():
    repeat = True

    while repeat == True:
        print("""What do you do?
    1. Attack the monster
    2. Comply with the monster
    3. Ignore the monster
    4. Stats
    5. Inventory 
""")
        choice_event10 = input()

        if int(choice_event10) == 1:
            print("""You prepare yourself for a fight.""")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_battle("hydra")

        elif int(choice_event10) == 2:
            print("""You choose to comply with the monster. The monster continues to stare you down, but makes no aggressive
            moves. You walk away peacefully.""")

        elif int(choice_event10) == 3:
            if random.randint(1, 100) < 80:
                print("""You attempt to simply ignore the monster, but that only makes him more angry.
                    
                \"How dare you ignore me! I will destroy you!\" He shouts.""")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_battle("hydra")
            else:
                print("""The monster seems surprisingly content with you leaving him alone. Maybe he doesn't get paid enough for this.""")
                return

        elif int(choice_event10) == 4:
            print_stats()
            repeat = True

        elif int(choice_event10) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Forest Event
def trigger_event11():
    repeat = True

    while repeat == True:
        print("""You take an arrow to the knee. Ow.
1. Pull it out
2. Break off the end of it
3. Leave it
4. Stats
5. Inventory 
""")
        
        choice_event11 = input()
        
        if int(choice_event11) == 1:
            if character_statistics["Strength"] <= 5:
                print("""You are too wimpy to take it out
                      
Lose 3 HP!""")
                character_statistics["HP"] -= 3

        elif int(choice_event11) == 2:
            print()

        elif int(choice_event11) == 3:
            print()
        
        elif int(choice_event11) == 4:
            print_stats()
            repeat = True

        elif int(choice_event11) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Mountain Event
def trigger_event12():
    repeat = True

    while repeat == True:
        print("""You stumble upon a bridge whilst adventuring through the mountains, and are encountered by an old man.
He tells you something about answering 3 questions correctly to cross the bridge, and otherwise you'll die. What do you do?
1. Answer him these questions 3
2. Cross the bridge without answering the questions
3. Turn and run
4. Stats
5. Inventory 
""")
        
        choice_event12 = input()
        
        if int(choice_event12) == 1:
            input("""What... is your name?
""")
            input("""What... is your quest?
""")
            trigger_event12_1()
            

        elif int(choice_event12) == 2:
            print("""Bad choice, the bridge was apparently guarded by a troll, and a powerful one, too.""")
            trigger_battle("troll")
            return

        elif int(choice_event12) == 3:
            if random.randint(1, 100) < 5 * character_statistics["Speed"]:
                print("""You escaped to another biome before even thinking to turn back around.
""")
                teleport_random_biome()
                return
            elif random.randint(1, 100) < 50:
                print("""You run away from the bridge, but choose to stay in the mountains.
""")
                return
            else:
                print("""You are unable to escape, and are forced to answer him these questions 3...""")
                choice_event12 = 1
                repeat = True
        
        elif int(choice_event12) == 4:
            print_stats()
            repeat = True

        elif int(choice_event12) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

def trigger_event12_1():
    question = random.randint(1, 5)
    if question == 1:
        print("""What... is your favorite color?""")
        input()
        print("""Right, go along then.
              
You cross the bridge and continue on your journey.""")
        return
    
    if question == 2:
        if random.randint(1, 100) < 30:
            print("""What... is your favorite color?""")
            input()
            print("""NO! You are thrust from the side of the mountain, and you break something in your back.
                  
Lost 15 HP!""")
            character_statistics["HP"] -= 15
            return
        else:
            print("""What... is your favorite color?""")
            input()
            print("""Right, go along then.
              
You cross the bridge and continue on your journey.""")
            
    if question == 3:
        print("""What... is the airspeed velocity of an unladen swallow?""")
        response = input()
        if "swallow" in response.lower() and "?" in response.lower():
            print("""Wuh... I don't know that...
                  
The old man is then ferociously thrown from the side of the bridge, screaming. His fate is unknown. You do feel smarter though.
Gained 5 XP""")
            character_statistics["XP"] += 5
            return
        elif "african" in response.lower() or "european" in response.lower():
            print("""Wuh... I don't know that...
                  
The old man is then ferociously thrown from the side of the bridge. His fate is unknown. You do feel smarter though.
Gained 5 XP""")
            character_statistics["XP"] += 5
            return
        else:
            print("""NO! You are thrust from the side of the mountain, and you break something in your back.
                  
Lost 15 HP!""")
            character_statistics["HP"] -= 20
            return
        
    elif question == 4:
        print("""In the works""")
        return
    
    elif question == 5:
        print("""In the works""")
        return

def trigger_event13():
        
    repeat = True

    while repeat == True:
        print("""
1. 
2. 
3. 
4. Stats
5. Inventory 
""")
        
        choice_event13 = input()
        
        if int(choice_event13) == 1:
            print()

        elif int(choice_event13) == 2:
            print()

        elif int(choice_event13) == 3:
            print()
        
        elif int(choice_event13) == 4:
            print_stats()
            repeat = True

        elif int(choice_event13) == 5:
            check_inventory()
            repeat = True

        else:
            print("""Please type a number between 1 and 5.""")
            repeat = True

# Dictionaries

character_statistics = {
    "HP": 20,
    "Mana": 20,
    "Energy": 100,
    "Morale": 100,
    "Strength": 0,
    "Defense": 0,
    "Magic": 0,
    "Speed": 0,
    "Dexterity": 0,
    "Intellect": 0,
    "Swim": 0,
    "XP": 0,
    "Level": 1
}

inventory = {
    "Wood": 0,
    "Iron": 0,
    "Gold": 5,
    "Money": 5,
    "Rubber ducks": 1
}

Csetting = "Forest"
setting = {
    "Forest": True,
    "Swamp": False,
    "Plains": False,
    "Ocean": False,
    "Tundra": False,
    "Jungle": False,
    "Desert": False,
    "Mountains": False,
    "Castle": False
}

enemy_stats = {
    "HP": 1,
    "Strength": 1,
    "Defense": 1,
    "Speed": 1,
    "Magic": 1
}

purchase_price = {
    "Wood": 2,
    "Iron": 3,
    "Gold": 5
}

sell_price = {
    "Wood": 1,
    "Iron": 2,
    "Gold": 3
}

import random

# All Weapons
import random

weapons = {
    # ---------------- Legendary Weapons (20) ----------------

    "Reaper of the Gods": {"rarity": "Legendary", "damage": random.randint(80, 95), "hit_chance": 90, "type": "Melee", "drop_rate": 1, "special_power": "blind"},
    "Sun Blade": {"rarity": "Legendary", "damage": random.randint(50, 60), "hit_chance": 80, "type": "Melee", "drop_rate": 5, "special_power": "fire"},
    "Eternal Spear": {"rarity": "Legendary", "damage": random.randint(70, 85), "hit_chance": 85, "type": "Melee", "drop_rate": 3, "special_power": "lightning"},
    "Dragon Fang": {"rarity": "Legendary", "damage": random.randint(85, 100), "hit_chance": 75, "type": "Melee", "drop_rate": 2, "special_power": "poison"},
    "Frostmourne": {"rarity": "Legendary", "damage": random.randint(80, 95), "hit_chance": 70, "type": "Melee", "drop_rate": 2, "special_power": "frost"},
    "Celestial Bow": {"rarity": "Legendary", "damage": random.randint(60, 80), "hit_chance": 95, "type": "Ranged", "drop_rate": 4, "special_power": "pierce"},
    "Hammer of Titans": {"rarity": "Legendary", "damage": random.randint(90, 110), "hit_chance": 65, "type": "Melee", "drop_rate": 1, "special_power": "stun"},
    "Shadow Scythe": {"rarity": "Legendary", "damage": random.randint(75, 95), "hit_chance": 80, "type": "Melee", "drop_rate": 3, "special_power": "shadow"},
    "Phoenix Staff": {"rarity": "Legendary", "damage": random.randint(55, 70), "hit_chance": 85, "type": "Magic", "drop_rate": 5, "special_power": "revive"},
    "Blade of Eternity": {"rarity": "Legendary", "damage": random.randint(95, 120), "hit_chance": 85, "type": "Melee", "drop_rate": 1, "special_power": "time_stop"},
    "Orb of Infinity": {"rarity": "Legendary", "damage": random.randint(70, 90), "hit_chance": 90, "type": "Magic", "drop_rate": 2, "special_power": "invisibility"},
    "Lance of Light": {"rarity": "Legendary", "damage": random.randint(75, 95), "hit_chance": 88, "type": "Melee", "drop_rate": 3, "special_power": "holy"},
    "Thunderstorm Bow": {"rarity": "Legendary", "damage": random.randint(80, 100), "hit_chance": 85, "type": "Ranged", "drop_rate": 2, "special_power": "shock"},
    "Crownbreaker Axe": {"rarity": "Legendary", "damage": random.randint(100, 120), "hit_chance": 70, "type": "Melee", "drop_rate": 1, "special_power": "crush"},
    "Serpent Fang Dagger": {"rarity": "Legendary", "damage": random.randint(65, 80), "hit_chance": 95, "type": "Melee", "drop_rate": 4, "special_power": "poison"},
    "Volcanic Blade": {"rarity": "Legendary", "damage": random.randint(85, 105), "hit_chance": 80, "type": "Melee", "drop_rate": 3, "special_power": "lava"},
    "Scepter of Stars": {"rarity": "Legendary", "damage": random.randint(60, 75), "hit_chance": 90, "type": "Magic", "drop_rate": 4, "special_power": "meteor"},
    "Wraith Scythe": {"rarity": "Legendary", "damage": random.randint(90, 105), "hit_chance": 78, "type": "Melee", "drop_rate": 2, "special_power": "soul_drain"},
    "Heaven’s Wrath": {"rarity": "Legendary", "damage": random.randint(100, 125), "hit_chance": 85, "type": "Melee", "drop_rate": 1, "special_power": "smite"},
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
    "Soulfire Staff": {"rarity": "Insane", "damage": random.randint(45, 60), "hit_chance": 75, "type": "Magic", "drop_rate": 35, "special_power": "soul_burn"},
    "Ruin Blade": {"rarity": "Insane", "damage": random.randint(85, 105), "hit_chance": 50, "type": "Melee", "drop_rate": 25, "special_power": "destruction"},
    "Howling Pike": {"rarity": "Insane", "damage": random.randint(60, 85), "hit_chance": 65, "type": "Melee", "drop_rate": 40, "special_power": "scream"},

# ---------------- Rare Weapons (20) ----------------

    "Bright Blade": {"rarity": "Rare", "damage": random.randint(20, 25), "hit_chance": 75, "type": "Melee", "drop_rate": 60, "special_power": "blind"},
    "Storm Bow": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 80, "type": "Ranged", "drop_rate": 50, "special_power": "shock"},
    "Crystal Dagger": {"rarity": "Rare", "damage": random.randint(22, 28), "hit_chance": 90, "type": "Melee", "drop_rate": 55, "special_power": "pierce"},
    "Shadow Katana": {"rarity": "Rare", "damage": random.randint(28, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "shadow"},
    "Flame Mace": {"rarity": "Rare", "damage": random.randint(30, 45), "hit_chance": 65, "type": "Melee", "drop_rate": 50, "special_power": "fire"},
    "Moon Spear": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 70, "type": "Melee", "drop_rate": 55, "special_power": "freeze"},
    "Venom Crossbow": {"rarity": "Rare", "damage": random.randint(20, 30), "hit_chance": 80, "type": "Ranged", "drop_rate": 60, "special_power": "poison"},
    "Lava Sword": {"rarity": "Rare", "damage": random.randint(35, 45), "hit_chance": 60, "type": "Melee", "drop_rate": 40, "special_power": "fire"},
    "Frost Wand": {"rarity": "Rare", "damage": random.randint(18, 25), "hit_chance": 85, "type": "Magic", "drop_rate": 55, "special_power": "frost"},
    "Spirit Lance": {"rarity": "Rare", "damage": random.randint(30, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "drain"},
    "Runed Staff": {"rarity": "Rare", "damage": random.randint(20, 28), "hit_chance": 80, "type": "Magic", "drop_rate": 50, "special_power": "mana_boost"},
    "Glacier Hammer": {"rarity": "Rare", "damage": random.randint(32, 45), "hit_chance": 65, "type": "Melee", "drop_rate": 45, "special_power": "freeze"},
    "Stormbreaker Axe": {"rarity": "Rare", "damage": random.randint(35, 50), "hit_chance": 70, "type": "Melee", "drop_rate": 40, "special_power": "shock"},
    "Venom Fang Sword": {"rarity": "Rare", "damage": random.randint(30, 40), "hit_chance": 75, "type": "Melee", "drop_rate": 45, "special_power": "poison"},
    "Ashen Bow": {"rarity": "Rare", "damage": random.randint(25, 35), "hit_chance": 80, "type": "Ranged", "drop_rate": 50, "special_power": "fire"},
    "Sunsteel Spear": {"rarity": "Rare", "damage": random.randint(28, 38), "hit_chance": 70, "type": "Melee", "drop_rate": 55, "special_power": "burn"},
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

spells = {
    "Wind Spell": {"damage": random.randint(10, 20), "hit_chance": 60, "mana_cost": 3, "special_power": "none"},
    "Ice Blast": {"damage": random.randint(10, 20), "hit_chance": 60, "mana_cost": 3, "special_power": "none"},
    "Lightning Bolt": {"damage": random.randint(10, 20), "hit_chance": 60, "mana_cost": 3, "special_power": "none"},
}
current_spells = {}

list_of_classes = ["1. Warrior", "2. Mage", "3. Defender"]
# Player starts with 3 slots
player_weapons = ["Fist", "Fist", "Fist"]

# Game Start
print("""To play, type in the number of the option you would like to choose.
      
Welcome to Löwengarde! A magical place of destiny, heroes, and courage.
We welcome you with all our hearts, and wish you a wonderful stay!
Unfortunately, now isn't the best time to come for a vacation or a lolly,
as there has been a major insurrection among the government of the united
race tribes, and an evil ogre named NAME has taken over, enforcing all under
his rule to work as his servants and slave away for no money, and what little
we do receive is taxed.

Say, you appear to be a noble warrior, and therefore we would petition your help.
What kind of warrior are you, new friend?
""")
print_choices(list_of_classes)



while True:
    chosen_class = input().strip()
    try:
        chosen_class = int(chosen_class)
    except ValueError:
        print("That's not a number. Please enter 1, 2, or 3.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        continue
    chosen_class = int(chosen_class)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if chosen_class == 1:
        print("""Ah, a warrior! Strong with the sword, mighty with the bow!
Truly the fighter we always desired! We believe in you warrior,
we know you can set us free from the tyrannical king NAME
            
You begin the game with 10 Strength and a Sturdy Sword""")
        character_statistics["Strength"] += 10
        player_weapons[0] = "Sturdy Sword"
        player_weapons[1] = "Sun Blade"
        break
    elif chosen_class == 2:
        print("""Ah, a mage! A mind like a tempest, and a desire burning like fire!
Truly the fighter we always desired! We believe in you mage,
we know you can set us free from the tyrannical king NAME
            
You begin the game with 10 Magic, a Sturdy Sword, and a simple Wind Spell""")
        max_Mana == 30
        character_statistics["Mana"] = max_Mana
        character_statistics["Magic"] += 10
        current_spells["Wind Spell"] = 1
        player_weapons[0] = "Wooden Staff"
        break
    elif chosen_class == 3:
        print("""Ah, a defender! Hard like a rock, impenetrable, and ready to protect at all costs!
Truly the fighter we always desired! We believe in you defender,
we know you can set us free from the tyrannical king NAME
            
You begin the game with 10 Defense and a Rusty Sword""")
        character_statistics["Defense"] += 10
        player_weapons[0] = "Rusty Sword"
        break
    else:
        print("Please type a 1, 2, or 3 to choose your class.")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        continue

# Gameplay Loop

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
weapon_get()
trigger_battle("goblin", 0)
does_game_end()
level_up()

continue_game = True
while continue_game == True:
    if setting["Forest"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event7()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event7()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()

    if setting["Swamp"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event5()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event5()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event5()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event5()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event5()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event6()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event6()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event6()
            does_game_end()
            level_up()

    if setting["Tundra"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event4()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event4()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event4()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event9()
            does_game_end()
            level_up()

    if setting["Jungle"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()

    if setting["Plains"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()

    if setting["Desert"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event3()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event10()
            does_game_end()
            level_up()

    if setting["Mountains"] == True:
        next_event = random.randint(1, 10)
        if next_event == 1:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event12()
            does_game_end()
            level_up()
        if next_event == 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event12()
            does_game_end()
            level_up()
        if next_event == 3:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event12()
            does_game_end()
            level_up()
        if next_event == 4:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 5:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 6:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 7:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()
            does_game_end()
            level_up()
        if next_event == 8:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 9:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()
        if next_event == 10:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event2()
            does_game_end()
            level_up()

    if setting["Ocean"] == True:
        next_event = random.randint(1, 10)
        if is_On_Water == False:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            trigger_event8()

        elif is_On_Water == True:
            if next_event == 1:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 2:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 3:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 4:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 5:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 6:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 7:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 8:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 9:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()
            if next_event == 10:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                trigger_event11()
                does_game_end()
                level_up()