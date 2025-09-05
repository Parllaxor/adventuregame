import random
def combat():

    repeat = True

    while repeat == True and enemy_stats["HP"] > 0:
    
        if(random.randint(1, 2) == 1):
            while True:
                print("""You manage to get a jump on the opponent what do you do?
            
1. Use a weapon
2. Use an item
3. Attempt to flee
4. Inventory
5. Stats
6. Enemy Stats
""")

                choice_attack = input()

                if int(choice_attack) == 1:
                    choice_weapon = input(f"""Which weapon shall you use to strike?
                    
1. {weapon1}
2. {weapon2}
3. {weapon3}
4. Back
""")
        

                
                    if int(choice_weapon) == 1 or int(choice_weapon) == 2 or int(choice_weapon) == 3:
                        is_valid_weapon(choice_weapon)
                        break
                    elif int (choice_weapon) == 4:
                        continue  # Goes back to the start of the while loop
                    else: 
                        print("""Please choose a number between 1 and 4""")
                        continue

                elif int(choice_attack) == 2:
                    print("Which item would you like to use?\n")
                    print("1. Back")
                    item_lookup = {}

                    for item, amount in inventory.items():
                        if amount > 0:
                            print(f"{print_number}. {item}")
                            item_lookup[print_number] = item
                            print_number += 1

                    choice_item = input()
                    if choice_item == 1:
                        continue
                    else:
                        print("why am i here")
                        is_valid_item(choice_item, item_lookup)
                        return

                elif int(choice_attack) == 3:
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

                elif int(choice_attack) == 4:
                    check_inventory()
                    repeat = True

                elif int(choice_attack) == 5:
                    print_stats()
                    repeat = True

                elif int(choice_attack) == 6:
                    print_enemy_stats()
                    repeat = True

                else:
                    print("""Please enter a number between 1 and 6""")
                    repeat = True
        else:
            print("""The enemy was quicker, and has attacked you!""")
            if enemy_stats["Strength"] >= enemy_stats["Magic"]:
                combat_defense("melee")
            elif enemy_stats["Strength"] < enemy_stats["Magic"]:
                combat_defense("magic")
            else:
                combat_defense("melee")
    return
weapon1 = "Rusty Sword"
weapon2 = "Wooden Staff"
weapon3 = "Dagger"
enemy_stats = {
    "HP": 1,
    "Strength": 1,
    "Defense": 1,
    "Speed": 1,
    "Magic": 1
}
combat()