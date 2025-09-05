

    #Sets enemy stats
def trigger_battle(combat_opponent, enemy_level):
    # Ensure Enemy isn't too powerful
    if enemy_level == 0:
        enemy_level = random.randint(.75 * character_statistics["Level"], 1.5 * character_statistics["Level"])
    if enemy_level > math.ceil(1.5 * character_statistics["Level"]):
        enemy_level = math.ceil(1.5 * character_statistics["Level"])
    if enemy_level < math.ceil(.75 * character_statistics["Level"]):
        enemy_level = math.ceil(.75 * character_statistics["Level"])

    # Hydra Battle
    if combat_opponent.lower() == "hydra":
        print(f"""You are in combat against a level {enemy_level} hydra.""")
        enemy_stats["HP"] = 10 * enemy_level
        enemy_stats["Strength"] = 5 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 0

        

    # Goblin Battle
    elif combat_opponent.lower() == "goblin":
        print(f"""You are in combat against a level {enemy_level} goblin.""")
        enemy_stats["HP"] =  5 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0
    # Ogre Battle
    elif combat_opponent.lower() == "ogre":
    

        print(f"""You are in combat against a level {enemy_level} ogre.""")
        enemy_stats["HP"] =  6 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0
    # Orc Battle
    elif combat_opponent.lower() == "orc":
        print(f"""You are in combat against a level {enemy_level} orc.""")
        enemy_stats["HP"] =  10 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Wizard Battle
        print(f"""You are in combat against a level {enemy_level} wizard.""")
        enemy_stats["HP"] =  5 * enemy_level
        enemy_stats["Strength"] = 0
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 3 * enemy_level
        enemy_stats["Magic"] = 4 * enemy_level

    # Golem Battle

        print(f"""You are in combat against a level {enemy_level} golem.""")
        enemy_stats["HP"] =  6 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 0

    # Bandit Battle
    elif combat_opponent.lower() == "bandit":

        print(f"""You are in combat against a level {enemy_level} bandit.""")
        enemy_stats["HP"] =  2 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 2 * enemy_level
        enemy_stats["Speed"] = 6 * enemy_level
        enemy_stats["Magic"] = 0

    # Dragon Battle
    elif combat_opponent.lower() == "dragon":
        print(f"""You are in combat against a level {enemy_level} dragon.""")
        enemy_stats["HP"] =  12 * enemy_level
        enemy_stats["Strength"] = 6 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 5 * enemy_level

    elif combat_opponent.lower() == "troll":
    # Troll Battle
        print(f"""You are in combat against a level {enemy_level} troll.""")
        enemy_stats["HP"] =  6 * enemy_level
        enemy_stats["Strength"] = 8 * enemy_level
        enemy_stats["Defense"] = 4 * enemy_level
        enemy_stats["Speed"] = 2 * enemy_level
        enemy_stats["Magic"] = 0

    else:
        print("ERROR: No valid enemy selected")
        exit()


