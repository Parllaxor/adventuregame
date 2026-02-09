import pygame
import sys
import random
import math
import time
import webbrowser
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Modern Colors (matching web design)
WHITE = (255, 255, 255)
BLACK = (26, 26, 26)
LIGHT_BG = (240, 240, 240)
DARK_OVERLAY = (0, 0, 0)

# Gradients & UI Colors
PRIMARY_GREEN = (76, 175, 80)
PRIMARY_BLUE = (33, 150, 243)
ACCENT_PURPLE = (156, 39, 176)
SUCCESS_GREEN = (200, 230, 201)
WARNING_ORANGE = (255, 152, 0)
DANGER_RED = (244, 67, 54)

# Stat Badge Colors
STRENGTH_COLOR = (211, 47, 47)  # Red
DEFENSE_COLOR = (25, 118, 210)  # PRIMARY_BLUE
MAGIC_COLOR = (124, 58, 237)    # Purple
INTELLECT_COLOR = (249, 140, 0) # Orange
DEXTERITY_COLOR = (56, 142, 60) # PRIMARY_GREEN
SPEED_COLOR = (0, 150, 136)     # Teal
SWIM_COLOR = (41, 128, 185)     # Ocean PRIMARY_BLUE

# Biome background gradients (darker, more mood)
biome_colors = {
    "Forest": (52, 168, 83),
    "Desert": (245, 166, 35),
    "Ocean": (74, 144, 226),
    "Mountains": (123, 104, 238),
    "Swamp": (133, 167, 71),
    "Plains": (129, 199, 132),
    "Tundra": (207, 226, 243),
    "Jungle": (0, 128, 0),
    "Castle": (139, 69, 19)
}

# Fonts - Using better font sizes for modern UI
font = pygame.font.SysFont('arial', 18)
large_font = pygame.font.SysFont('arial', 32)
title_font = pygame.font.SysFont('arial', 48, bold=True)
small_font = pygame.font.SysFont('arial', 14)

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width pixels."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Button class - Modern styled
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = self._lighten_color(color, 40)
        self.is_hovered = False
        self.scale = 1.0

    def _lighten_color(self, color, amount):
        """Lighten a color by the given amount"""
        return tuple(min(c + amount, 255) for c in color)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(mouse_pos)
        self.is_hovered = is_hovering
        
        # Smooth shadow effect
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=8)
        
        # Main button
        button_color = self.hover_color if is_hovering else self.color
        pygame.draw.rect(screen, button_color, self.rect, border_radius=10)
        
        # Border
        border_color = self._lighten_color(button_color, 30)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=10)
        
        # Text - always white for contrast
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Game state
current_text = "Welcome to Löwengarde! A magical place of destiny, heroes, and courage.\nWe welcome you with all our hearts, and wish you a wonderful stay!\nUnfortunately, now isn't the best time to come for a vacation or a lolly,\nas there has been a major insurrection among the government of the united\nrace tribes, and an evil ogre named NAME has taken over, enforcing all under\nhis rule to work as his servants and slave away for no money, and what little\nwe do receive is taxed.\n\nSay, you appear to be a noble warrior, and therefore we would petition your help.\nWhat kind of warrior are you, new friend?"
inventory_visible = False
stats_visible = False
game_started = False
buttons = [
    Button(50, 400, 120, 50, "Warrior", STRENGTH_COLOR),
    Button(200, 400, 120, 50, "Mage", ACCENT_PURPLE),
    Button(350, 400, 120, 50, "Defender", DEFENSE_COLOR)
]

# Game state variables
chosen_class = 0
current_biome = "Forest"
current_event_name = None
current_event = None
inventory_visible = False
stats_visible = False
game_started = False

def handle_choice(choice):
    global current_text, buttons, chosen_class, game_started, current_biome, current_event
    
    if not game_started:
        # Class selection
        if choice == "Warrior":
            chosen_class = 1
            character_statistics["Strength"] += 5
            character_statistics["Defense"] += 3
            current_text = "You have chosen the path of the Warrior! Strength and Defense increased.\n\nYou begin your journey in the Forest."
            game_started = True
            current_biome = "Forest"
            Csetting = "Forest"
            setting["Forest"] = True
            # Start the game with first event
            trigger_random_event()
        elif choice == "Mage":
            chosen_class = 2
            character_statistics["Magic"] += 5
            character_statistics["Intellect"] += 3
            current_text = "You have chosen the path of the Mage! Magic and Intellect increased.\n\nYou begin your journey in the Forest."
            game_started = True
            current_biome = "Forest"
            Csetting = "Forest"
            setting["Forest"] = True
            # Start the game with first event
            trigger_random_event()
        elif choice == "Defender":
            chosen_class = 3
            character_statistics["Defense"] += 5
            character_statistics["Strength"] += 3
            current_text = "You have chosen the path of the Defender! Defense and Strength increased.\n\nYou begin your journey in the Forest."
            game_started = True
            current_biome = "Forest"
            Csetting = "Forest"
            setting["Forest"] = True
            # Start the game with first event
            trigger_random_event()
    else:
        # Handle in-game choices
        if choice == "Stats":
            # Open profile.html in browser
            profile_path = os.path.join(os.path.dirname(__file__), "profile.html")
            webbrowser.open(f"file://{profile_path}")
            return
        elif choice == "Inventory":
            # Open inventory.html in browser
            inventory_path = os.path.join(os.path.dirname(__file__), "inventory.html")
            webbrowser.open(f"file://{inventory_path}")
            return
        elif choice == "Continue":
            # Continue to next event
            trigger_random_event()
            return
        elif choice == "Explore":
            # Start exploring - trigger random event
            trigger_random_event()
            return
        elif choice == "Rest":
            # Rest to recover
            character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 5)
            character_statistics["Energy"] = min(100, character_statistics["Energy"] + 10)
            current_text = "You rest and recover some HP and energy."
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
            return
        
        # Handle event choices
        if current_event:
            current_event(choice)

def start_biome_loop():
    global current_text, buttons
    current_text = f"You have arrived in the {current_biome}.\n\nWhat would you like to do?"
    buttons = [
        Button(50, 400, 120, 50, "Explore", PRIMARY_GREEN),
        Button(200, 400, 120, 50, "Rest", PRIMARY_GREEN),
        Button(350, 400, 120, 50, "Stats", PRIMARY_BLUE),
        Button(500, 400, 120, 50, "Inventory", PRIMARY_BLUE)
    ]

def handle_event_choice(choice):
    global current_text, buttons, current_event, current_event_name, max_HP
    
    # Handle stats and inventory buttons - open HTML files
    if choice == "Stats":
        # Open profile.html in browser
        profile_path = os.path.join(os.path.dirname(__file__), "profile.html")
        webbrowser.open(f"file://{profile_path}")
        return  # Don't complete the event
    
    if choice == "Inventory":
        # Open inventory.html in browser
        inventory_path = os.path.join(os.path.dirname(__file__), "inventory.html")
        webbrowser.open(f"file://{inventory_path}")
        return  # Don't complete the event
    
    # Handle event-specific logic
    if current_event_name == "trigger_event1":
        if choice == "Attack Sword":
            if character_statistics["Strength"] >= 5 or character_statistics["Defense"] >= 5:
                current_text = "Well done fighter! You have slain the goblin.\n\nGained 10 XP"
                character_statistics["XP"] += 10
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    current_text = "You have been smitten fighter! You were not strong enough to fight this goblin with the sword.\n\nLost 5 HP"
                    character_statistics["HP"] -= 5
                else:
                    current_text = "The goblin has bested you traveller. This is the end of the road for you. Let your name rest in legend.\n\nLost 20 HP"
                    character_statistics["HP"] -= 20
        elif choice == "Fireball":
            if character_statistics["Magic"] >= 5:
                current_text = "Well done fighter! You have slain the goblin.\n\nGained 10 XP"
                character_statistics["XP"] += 10
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    current_text = "You have been smitten fighter! You were not experienced enough to fight the goblin with a fireball.\n\nLost 5 HP"
                    character_statistics["HP"] -= 5
                else:
                    current_text = "The goblin has bested you traveller. This is the end of the road for you. Let your name rest in legend.\n\nLost 20 HP"
                    character_statistics["HP"] -= 20
        elif choice == "Run":
            current_text = "You have run away like a coward. You are not fit to be a fighter for this kingdom. We wish you well, traveller. Goodbye.\n\nLost 20 HP"
            character_statistics["HP"] -= 20
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event3":
        if choice == "Spin Attack":
            if character_statistics["Strength"] >= 15:
                current_text = "You spin around, sword outstretched, daring any gnomes to come close to you. They run to you in hordes, but are sliced down and slain by your sword.\n\nGained 20 XP\nWhat now?\n1. Loot the bodies\n2. Continue"
                character_statistics["XP"] += 20
                buttons = [Button(50, 400, 100, 50, "Loot", PRIMARY_GREEN), Button(170, 400, 100, 50, "Continue", PRIMARY_GREEN)]
                current_event_name = "event3_sub1"
                return
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    current_text = "You accidentally throw out your shoulder while spinning. The attacking gnomes feel pity and leave you alone.\n\nLost 5 HP\nLost 2 Strength"
                    character_statistics["HP"] -= 5
                    character_statistics["Strength"] -= 2
                else:
                    current_text = "The sword flies from your hand. The gnomes annihilate you. Let your name rest in legend.\n\nYou have died"
                    character_statistics["HP"] = 0
        elif choice == "Lightning Strike":
            if "Lightning Bolt" in current_spells:
                current_text = "As the sound of thunder cracks above, the gnomes freeze. They glance into the sky, only to see their lives flash before their eyes. After a moment, you are the only nearby creature left standing.\n\nGained 25 XP"
                character_statistics["XP"] += 25
            else:
                fate = random.randint(1, 3)
                if fate == 1:
                    current_text = "You try really hard to make a lightning bolt come down, but it just doesn't happen. Wonder how those wizards do it. The gnomes watch your pathetic attempt and realize there is no benefit to killing you. They leave you alone, but you are very embarrassed.\n\nLost 15 Morale"
                    character_statistics["Morale"] -= 15
                elif fate == 2:
                    current_text = "You accidentally strike yourself with lightning and paralyze yourself. The gnomes leave you for dead. However, you manage to survive. Barely.\n\n1 HP Remaining"
                    character_statistics["HP"] = 1
                else:
                    current_text = "You failed to cast a lightning bolt, and the gnomes have slain you. May your name rest in legend.\n\nYou have died."
                    character_statistics["HP"] = 0
        elif choice == "Bribe":
            if inventory["Money"] >= 2:
                current_text = "You have enough money to fulfill the gnome king's demands. He takes 2 coins, but leaves you with your life.\n\nLost 2 Money"
                inventory["Money"] -= 2
            elif inventory["Gold"] >= 1:
                current_text = "You have enough gold to fulfill the gnome king's demands. He takes 1 gold, but leaves you with your life.\n\nLost 1 Gold"
                inventory["Gold"] -= 1
            else:
                current_text = "Your offering was not good enough for the gnome king, and you were sacrificed to the gnome Gods. You have been slain. May your name rest in legend.\n\nYou have died."
                character_statistics["HP"] = 0
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event4":
        if choice == "Nap":
            current_text = "You choose to take a nap\n\nHealed 5 HP"
            character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 5)
        elif choice == "Melt Igloo":
            fate = random.randint(1, 2)
            if fate == 1:
                current_text = "You find some gold in the melted remains of the poor igloo.\n\nObtained 2 Gold\nGained 5 XP"
                character_statistics["XP"] += 5
                inventory["Gold"] += 2
            else:
                current_text = "You accidentally manage to melt the entire tundra. You are now in the ocean. You monster."
                setting["Ocean"] = True
                setting["Tundra"] = False
                current_biome = "Ocean"
        elif choice == "Take Book":
            if "Frozen Shards" not in current_spells:
                current_text = "You take the icicle bolt spell book. Learned Frozen Shards!"
                current_spells["Frozen Shards"] = 1
            else:
                current_text = "You already know this spell."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event5":
        if choice == "Drink Potion":
            fate = random.randint(1, 10)
            if fate == 1 or fate == 2:
                current_text = "You drink the potion. It is sweet to the taste. You feel your energy surging!\n\nSpeed increased by 10!\nGained 5 XP"
                character_statistics["Speed"] += 10
                character_statistics["XP"] += 5
            elif fate == 3:
                current_text = "You drink the potion. It tastes bitter, but surprisingly tasty. You feel empowered!\n\nStrength increased by 10!\nGained 5 XP"
                character_statistics["Strength"] += 10
                character_statistics["XP"] += 5
            elif fate == 4:
                current_text = "You drink the potion. It does not taste good. You don't feel too sick yet though...\n\nLost 10 Morale"
                character_statistics["Morale"] -= 10
            elif fate == 5:
                current_text = "You drink the potion. Nothing happens. It was probably just water, but you're polite and leave with a thanks."
            elif fate == 6:
                current_text = "You drink the potion. You start feeling very sick, and lose much of your energy to continue fighting.\n\nEnergy decreased by 50"
                character_statistics["Energy"] -= 50
            elif fate == 7:
                current_text = "You drink the potion. Apparently it's just clam chowder. Yum!\n\nSwim increased by 10!"
                character_statistics["Swim"] += 10
            elif fate == 8:
                current_text = "You drink the potion. It is very obviously poison. You'll learn to walk it off.\n\nDown to 1 HP!"
                character_statistics["HP"] = 1
            elif fate == 9:
                current_text = "You drink the potion. You can't tell immediately what happens, but you feel great!\n\nGained 10 HP"
                character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 10)
            elif fate == 10:
                current_text = "You drink the potion. It was a love potion. Unfortunately, there are no fair maidens in the kingdom for quite a ways. You still find yourself walking with a spring in your step!\n\nGained 10 Morale"
                character_statistics["Morale"] = min(100, character_statistics["Morale"] + 10)
        elif choice == "Slay Witch":
            if character_statistics["Strength"] >= 15 or character_statistics["Magic"] >= 15:
                current_text = "You kill the witch. You didn't even give her a chance to explain herself. Maybe the true monster is you...\n\nGained 20 XP"
                character_statistics["XP"] += 20
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    current_text = "The witch splashes you with poison potions while you stumble around trying to fight her. It hurts very badly, but maybe you deserve this...\n\nLost 10 HP"
                    character_statistics["HP"] -= 10
                else:
                    current_text = "You fail to slay the witch, but luckily are able to escape before more damage can be done."
                    teleport_random_biome()
                    buttons = [
                        Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                        Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                        Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                    ]
                    current_event = None
                    current_event_name = None
                    return
        elif choice == "Run Away":
            if character_statistics["Speed"] > 5:
                current_text = "You manage to escape the witch, and are lucky enough to survive."
                teleport_random_biome()
                buttons = [
                    Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                    Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                    Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                ]
                current_event = None
                current_event_name = None
                return
            else:
                if random.randint(1, 100) < 75:
                    current_text = "You successfully escape the situation, but remain in the swamp."
                else:
                    current_text = "You run away, but you end up stubbing your toe on the way out. Ouch...\n\nLost 5 HP"
                    character_statistics["HP"] -= 5
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event6":
        if choice == "Grab":
            fate = random.randint(1, 2)
            if fate == 1:
                current_text = "Turns out it was just some gold. Lucky you!\n\nObtained 5 Gold"
                inventory["Gold"] += 5
            else:
                current_text = "Oh no! It's a shark... Your worst nightmare! How will you rid of this foe?\n1. Bite it!\n2. Blast it with a fireball\n3. Swim as fast as you can\n4. Stats\n5. Inventory"
                buttons = [Button(50, 400, 100, 50, "Bite", PRIMARY_GREEN), Button(170, 400, 120, 50, "Fireball", PRIMARY_GREEN), Button(300, 400, 120, 50, "Swim", PRIMARY_GREEN), Button(50, 450, 100, 50, "Stats", PRIMARY_BLUE), Button(170, 450, 100, 50, "Inventory", PRIMARY_BLUE)]
                current_event_name = "event6_enemy"
                return
        elif choice == "Dig":
            fate = random.randint(1, 2)
            if fate == 1:
                current_text = "You manage to find atlantis under the mud. You grab 5 gold and you cover it back up. Not worth your time.\n\nGained 5 Gold"
                inventory["Gold"] += 5
            else:
                current_text = "You can't dig fast enough to clear mud. You feel sad.\n\nLost 5 Morale"
                character_statistics["Morale"] -= 5
        elif choice == "Ignore":
            current_text = "You choose to ignore whatever was in the mud and continue on your journey."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "event6_enemy":
        if choice == "Bite":
            if character_statistics["Strength"] >= 10 or character_statistics["Defense"] >= 10:
                current_text = "The shark looks at you, confused. 'Why did you bite me?' It seems to wonder. Rude. The shark swims away, giving you a stank look while he goes.\n\nGained 5 XP!"
                character_statistics["XP"] += 5
            else:
                fate = random.randint(1, 2)
                if fate == 1:
                    current_text = "The shark bites your face and you die. May your name rest in legend.\n\nYou have died."
                    character_statistics["HP"] = 0
                else:
                    current_text = "You end up scaring the spooky shark with your menacing bite force, but you swallow lots of mud in the process. You start feeling a bit sick...\n\nLost 10 Morale\nLost 10 Energy"
                    character_statistics["Morale"] -= 10
                    character_statistics["Energy"] -= 10
        elif choice == "Fireball":
            if character_statistics["Magic"] > 10:
                current_text = "You manage to masterfully weave a fireball into the mud and hit the shark somehow... Well fighter, I am impressed.\n\nGained 5 XP\nGained 2 Magic"
                character_statistics["XP"] += 5
                character_statistics["Magic"] += 2
            else:
                current_text = "The fireball blows up in your face upon striking the mud. What were you thinking?\n\nLost 5 HP"
                character_statistics["HP"] -= 5
        elif choice == "Swim":
            if character_statistics["Swim"] >= 5:
                current_text = "You swim through the mud and escape the shark. Turns out sharks don't swim well in mud...\n\nYou have escaped."
            else:
                if inventory["Gold"] > 0:
                    current_text = "The shark slowly swims in circles around you. Luckily for you, it just wants your money.\n\nLost all gold"
                    inventory["Gold"] = 0
                else:
                    fate = random.randint(1, 2)
                    if fate == 1:
                        current_text = "The shark only wanted your money, but unfortunately for you, you have no money. Embarrassing. The shark rolls his eyes and flicks you a coin. Lucky you!\n\nGained 1 Gold"
                        inventory["Gold"] += 1
                    else:
                        current_text = "The shark demands payment in exchange for your life. You empty your pockets, but unfortunately they were already empty. The shark, as promised, takes your life. You are slain."
                        character_statistics["HP"] = 0
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event7":
        if "Lightning Bolt" not in current_spells:
            current_spells["Lightning Bolt"] = 1
            current_text = "You encounter a wizard deep in the forest. He appears to be nice! He hands you a book. What a nice guy.\n\nObtain Lightning Bolt"
        else:
            inventory["Book"] += 1
            current_text = "You encounter a wizard deep in the forest. He appears to be nice! He hands you a book. What a nice guy.\n\nObtain Book"
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event8":
        if choice == "Fish":
            fate = random.randint(1, 3)
            if fate == 1:
                current_text = "You manage to catch a big fish. You eat it, and it makes you happy! You decide to move on from the ocean.\n\nGained 10 Morale\nGained 5 HP"
                character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 5)
                character_statistics["Morale"] = min(100, character_statistics["Morale"] + 10)
                teleport_random_biome()
                buttons = [
                    Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                    Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                    Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                ]
                current_event = None
                current_event_name = None
                return
            elif fate == 2:
                current_text = "You are unable to catch any fish. You are sad. You decide to move on from the ocean.\n\nLost 10 Morale"
                character_statistics["Morale"] -= 10
                teleport_random_biome()
                buttons = [
                    Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                    Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                    Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                ]
                current_event = None
                current_event_name = None
                return
            else:
                current_text = "You let your guard down, and you are attacked by a group of pirates."
                current_event_name = "trigger_pirate_attack"
                current_text, choices = trigger_pirate_attack()
                buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
                current_event = handle_event_choice
                return
        elif choice == "Ignore":
            current_text = "You decide to walk away from the ocean. Can't blame you, who knows what's in there..."
            teleport_random_biome()
            buttons = [
                Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
            ]
            current_event = None
            current_event_name = None
            return
        elif choice == "Build Boat":
            if character_statistics["Swim"] >= 5:
                global is_On_Water
                is_On_Water = True
                enter_setting("Ocean")
                return
            else:
                current_text = "As you build a boat, you realize you don't know how to swim. Probably not the greatest idea to go sailing. You decide to continue on."
                teleport_random_biome()
                buttons = [
                    Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                    Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                    Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                ]
                current_event = None
                current_event_name = None
                return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event9":
        if choice == "Slay Fish":
            if character_statistics["Strength"] > 7 or character_statistics["Defense"] > 7:
                current_text = "You successfully obtain some food.\n\nEnergy Fully Restored!"
                character_statistics["Energy"] = 100
            else:
                current_text = "Turns out it's pretty hard to fish with your hands, particularly when the fish have very sharp teeth. You're bit once and choose to give up.\n\nLost 2 HP\nLost 10 Morale"
                character_statistics["HP"] -= 2
                character_statistics["Morale"] -= 10
        elif choice == "Run Through":
            if character_statistics["Swim"] > 2:
                fate = random.randint(1, 3)
                if fate == 1:
                    hp_loss = random.randint(2, 10)
                    current_text = f"You attempted to run through the river, but it was deeper than expected. You swam quickly enough to escape, but were hurt in the process.\n\nLost {hp_loss} HP\nLost 15 Energy"
                    character_statistics["HP"] -= hp_loss
                    character_statistics["Energy"] -= 15
                elif fate == 2:
                    current_text = "You manage to run through the river, and while you suffered from the cold, you were not badly hurt.\n\nLost 1 HP\nLost 5 Energy"
                    character_statistics["HP"] -= 1
                    character_statistics["Energy"] -= 5
                else:
                    if character_statistics["Speed"] > 5:
                        current_text = "Luckily for you, the river was just shallow enough for you to run without any fish biting you.\n\nGained 1 Speed"
                        character_statistics["Speed"] += 1
                    else:
                        current_text = "You attempt to run across the river, but trip and are eaten by the fish. You are slain."
                        character_statistics["HP"] = 0
            else:
                fate = random.randint(1, 3)
                if fate == 1:
                    current_text = "You cannot swim, and the river was a little bit too deep. You are unable to escape the fish and are eaten. You are slain."
                    character_statistics["HP"] = 0
                elif fate == 2:
                    hp_loss = random.randint(5, 15)
                    if character_statistics["HP"] - hp_loss < 1:
                        current_text = "You were lucky, and the river was just shallow enough for you to get across, suffering only a few fish bites. You survive.\n\nYou are left with 1 HP."
                        character_statistics["HP"] = 1
                    else:
                        current_text = f"You were lucky, and the river was just shallow enough for you to get across, suffering only a few fish bites. You survive.\n\nYou lost {hp_loss} HP"
                        character_statistics["HP"] -= hp_loss
                else:
                    current_text = "You somehow manage to escape over the river unscathed, you must be a track star or something.\n\nGained 1 Swimming!"
                    character_statistics["Swim"] += 1
        elif choice == "Build Bridge":
            if inventory["Wood"] > 1:
                current_text = "You successfully build a bridge, and use it to cross the river safely.\n\nLost 2 Wood"
                inventory["Wood"] -= 2
            else:
                current_text = "You have nothing to build a bridge with. Not sure what you were expecting to build. You obviously do not succeed at building a bridge, and were forced to attempt crossing on your own. You cross safely, but are badly hurt and tired.\n\nDown to 1 HP!\nDown to 1 Energy!"
                character_statistics["HP"] = 1
                character_statistics["Energy"] = 1
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event10":
        if choice == "Enter":
            fate = random.randint(1, 2)
            if fate == 1:
                hp_lost = 5
                if character_statistics["HP"] - hp_lost <= 0:
                    current_text = "Overzealous, you choose to dive into the fountain head first, consequently striking your head on the bottom of the fountain. You are knocked unconscious, and are unable to recover. You drown"
                    character_statistics["HP"] = 0
                else:
                    current_text = f"Overzealous, you choose to dive into the fountain head first, consequently striking your head on the bottom of the fountain. You are knocked unconscious, but are able to recover before drowning. It definitely hurt, though.\n\nLost {hp_lost} HP!"
                    character_statistics["HP"] -= hp_lost
            else:
                current_text = "You enter the fountain gracefully and feel rejuvenated.\n\nGained 10 HP"
                character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 10)
        elif choice == "Drink":
            fate = random.randint(1, 3)
            if fate == 1:
                current_text = "After taking a few sips, you notice some odd floaties in the water. You feel really uncomfortable. But you feel surprisingly good...\n\nPermanent HP increase!\nGained Full HP"
                max_HP += 2
                character_statistics["HP"] = max_HP
            elif fate == 2:
                current_text = "You take a few sips, but start to feel really sick. You notice some odd floaties in the water. You feel uncomfortable...\n\nPermanent HP decrease"
                max_HP -= 2
                if character_statistics["HP"] > max_HP:
                    character_statistics["HP"] = max_HP
            else:
                current_text = "After a refreshing drink, you turn away from the water."
        elif choice == "Store":
            current_text = 'A small head emerges from the deep, "That ain\'t yours you little punk." says the strange creature.'
            buttons = [Button(50, 400, 100, 50, "Attack", PRIMARY_GREEN), Button(170, 400, 100, 50, "Comply", PRIMARY_GREEN), Button(290, 400, 100, 50, "Ignore", PRIMARY_GREEN), Button(50, 450, 100, 50, "Stats", PRIMARY_BLUE), Button(170, 450, 100, 50, "Inventory", PRIMARY_BLUE)]
            current_event_name = "event10_sub1"
            return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "event10_sub1":
        if choice == "Attack":
            current_text = "You attack the monster and defeat it!\n\nGained 15 XP"
            character_statistics["XP"] += 15
        elif choice == "Comply":
            current_text = "You comply with the monster and leave peacefully."
        elif choice == "Ignore":
            current_text = "You ignore the monster and it attacks you!\n\nLost 10 HP"
            character_statistics["HP"] -= 10
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event11":
        if choice == "Pull Out":
            if character_statistics["Strength"] <= 5:
                current_text = "You are too wimpy to take it out\n\nLose 3 HP"
                character_statistics["HP"] -= 3
            else:
                fate = random.randint(1, 100)
                if fate <= 78:
                    current_text = "You manage to remove the arrow from your knee, but it hurts really badly.\n\nLose 3 HP"
                    character_statistics["HP"] -= 3
                else:
                    current_text = "You manage to remove the arrow from your knee, and cleanly. You put a bandaid on it, and you're good to go!\n\nGained 1 Dexterity"
                    character_statistics["Dexterity"] += 1
        elif choice == "Break Off":
            if character_statistics["Defense"] >= 10:
                current_text = "You snap off the end of the arrow. You are tough enough that you barely feel the arrow head embedded in your knee. However, the pain flares up when you move too quickly.\n\nLose 1 Speed"
                character_statistics["Speed"] -= 1
            elif character_statistics["Dexterity"] <= 3:
                fate = random.randint(1, 100)
                if fate <= 70:
                    current_text = "You snap the arrow off, and now you can't remove it. You should have gone to a doctor.\n\nMax HP reduced by 2"
                    max_HP -= 2
                    if character_statistics["HP"] > max_HP:
                        character_statistics["HP"] = max_HP
                else:
                    current_text = "When trying to snap the arrow off, somehow you simply pull the whole thing out. It hurts very bad, but at least you're alright. You even feel a little more dexterity coming on\n\nLose 1 HP\nGained 1 Dexterity"
                    character_statistics["HP"] -= 1
                    character_statistics["Dexterity"] += 1
            else:
                current_text = "When trying to snap the arrow off, somehow you simply pull the whole thing out. It hurts very bad, but at least you're alright. You even feel a little more dexterity coming on\n\nLose 1 HP\nGained 1 Dexterity"
                character_statistics["HP"] -= 1
                character_statistics["Dexterity"] += 1
        elif choice == "Leave":
            current_text = "You leave the arrow in. It hurts, but maybe it'll come out later.\n\nLose 2 HP"
            character_statistics["HP"] -= 2
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event12":
        if choice == "Answer Questions":
            # Simplified: just succeed or fail based on intellect
            if character_statistics["Intellect"] >= 5:
                current_text = "You answer all three questions correctly! The old man lets you pass.\n\nGained 10 XP"
                character_statistics["XP"] += 10
            else:
                current_text = "You fail to answer the questions correctly. The old man turns you away.\n\nLost 5 Morale"
                character_statistics["Morale"] -= 5
        elif choice == "Cross Bridge":
            fate = random.randint(1, 2)
            if fate == 1:
                current_text = "You try to cross without answering. The bridge collapses!\n\nLost 10 HP"
                character_statistics["HP"] -= 10
            else:
                current_text = "You manage to sneak across the bridge successfully.\n\nGained 5 XP"
                character_statistics["XP"] += 5
        elif choice == "Run":
            current_text = "You turn and run away from the bridge."
            teleport_random_biome()
            return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event14":
        if choice == "Pet":
            if character_statistics["Dexterity"] > 10 or random.randint(1,100) <= 25:
                current_text = "The deer lets you pet it. You feel happy.\n\nGained 5 Morale"
                character_statistics["Morale"] += 5
            else:
                current_text = "The deer gets scared and runs away."
        elif choice == "Hunt":
            if random.randint(1, 100) < character_statistics["Dexterity"] * 5:
                current_text = "You successfully slay the deer. Gained food, but you feel like a monster.\n\nEnergy Fully Restored! \n\nLost 10 Morale"
                character_statistics["Morale"] -= 10
                character_statistics["Energy"] = 100
            else:
                current_text = "The deer escapes."
        elif choice == "Ignore":
            current_text = "You continue on your path."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event2":
        if choice == "Scavenge for resources":
            fate = random.randint(1, 3)
            if fate == 1:
                current_text = "Well done fighter! You have found some wood.\n\nGained 1 Wood\nWhat do you do with it?\n1. Keep it\n2. Use it now"
                buttons = [Button(50, 400, 100, 50, "Keep it", PRIMARY_GREEN), Button(170, 400, 100, 50, "Use it now", PRIMARY_GREEN)]
                current_event_name = "event2_sub1"
                return
            elif fate == 2:
                current_text = "Well done fighter! You have found some iron.\n\nGained 1 Iron\nWhat do you do with it?\n1. Keep it\n2. Craft a tool"
                buttons = [Button(50, 400, 100, 50, "Keep it", PRIMARY_GREEN), Button(170, 400, 100, 50, "Craft a tool", PRIMARY_GREEN)]
                current_event_name = "event2_sub2"
                return
            elif fate == 3:
                current_text = "You find nothing of value. Better luck next time."
                buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
                current_event = None
                current_event_name = None
                game_over = does_game_end()
                if game_over:
                    current_text = game_over
                    buttons = []
                    return
                level_up()
                return
        elif choice == "Explore further":
            current_text = "You explore deeper into the swamp and find a hidden path. You gain 5 XP for your bravery."
            character_statistics["XP"] += 5
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
            current_event = None
            current_event_name = None
            game_over = does_game_end()
            if game_over:
                current_text = game_over
                buttons = []
                return
            level_up()
            return
        elif choice == "Rest yourself":
            character_statistics["HP"] = min(max_HP, character_statistics["HP"] + 5)
            character_statistics["Energy"] = min(100, character_statistics["Energy"] + 10)
            current_text = "You rest and recover some HP and energy."
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
            current_event = None
            current_event_name = None
            game_over = does_game_end()
            if game_over:
                current_text = game_over
                buttons = []
                return
            level_up()
            return
    elif current_event_name == "event2_sub1":
        if choice == "Keep it":
            inventory["Wood"] += 1
            current_text = "You keep the wood."
        elif choice == "Use it now":
            current_text = "You build a small shelter. Morale +5."
            character_statistics["Morale"] += 5
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "event2_sub2":
        if choice == "Keep it":
            inventory["Iron"] += 1
            current_text = "You keep the iron."
        elif choice == "Craft a tool":
            if character_statistics["Intellect"] > 5:
                current_text = "Crafted a tool. Strength +1."
                character_statistics["Strength"] += 1
            else:
                current_text = "Failed to craft. You keep the iron."
                inventory["Iron"] += 1
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "event3_sub1":
        if choice == "Loot":
            current_text = "Found 5 Money."
            inventory["Money"] += 5
        elif choice == "Continue":
            current_text = "You leave."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event15":
        if choice == "Touch":
            current_text = "You touch the plants and get poisoned.\n\nLost 10 HP"
            character_statistics["HP"] -= 10
        elif choice == "Avoid":
            current_text = "You wisely avoid the plants."
        elif choice == "Harvest":
            if character_statistics["Intellect"] > 10:
                current_text = "You carefully harvest the plants. They might be useful.\n\nGained 5 XP"
                character_statistics["XP"] += 5
            else:
                current_text = "You get poisoned while harvesting.\n\nLost 10 HP"
                character_statistics["HP"] -= 10
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event16":
        if choice == "Tame":
            if character_statistics["Dexterity"] > 15:
                current_text = "You tame a horse! Speed increased temporarily.\n\nGained 10 XP"
                character_statistics["Speed"] += 2
                character_statistics["XP"] += 10
            else:
                current_text = "The horses are too wild."
        elif choice == "Scare":
            current_text = "You scare the herd away."
        elif choice == "Watch":
            current_text = "You enjoy the sight. Morale boosted.\n\nGained 5 Morale"
            character_statistics["Morale"] += 5
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event17":
        if choice == "Fight":
            current_text = "A sea monster emerges from the depths!\n\nYou engage in battle with the sea monster!"
            buttons = [Button(50, 400, 100, 50, "Attack", PRIMARY_GREEN), Button(170, 400, 100, 50, "Defend", PRIMARY_GREEN), Button(290, 400, 100, 50, "Magic", PRIMARY_GREEN), Button(50, 450, 100, 50, "Stats", PRIMARY_BLUE), Button(170, 450, 100, 50, "Inventory", PRIMARY_BLUE)]
            current_event_name = "battle_sea_monster"
            return
        elif choice == "Dive":
            if character_statistics["Swim"] > 10:
                current_text = "You hide underwater successfully."
            else:
                current_text = "You can't swim well enough. The monster attacks.\n\nLost 15 HP"
                character_statistics["HP"] -= 15
        elif choice == "Sail":
            if character_statistics["Speed"] > 10:
                current_text = "You sail away safely."
            else:
                current_text = "The monster catches up.\n\nLost 10 HP"
                character_statistics["HP"] -= 10
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event18":
        if choice == "Build Fort":
            if character_statistics["Strength"] > 10:
                current_text = "You build a fort. You survive the blizzard.\n\nEnergy restored!"
                character_statistics["Energy"] = 100
            else:
                current_text = "The fort collapses.\n\nLost 10 HP"
                character_statistics["HP"] -= 10
        elif choice == "Keep Moving":
            current_text = "You push through the blizzard.\n\nLost 20 Energy"
            character_statistics["Energy"] -= 20
        elif choice == "Find Cave":
            if random.randint(1, 100) < 50:
                current_text = "You find a cave with treasure!\n\nGained 10 XP"
                character_statistics["XP"] += 10
            else:
                current_text = "No cave found. You freeze.\n\nLost 15 HP"
                character_statistics["HP"] -= 15
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event19":
        if choice == "Cut":
            if character_statistics["Strength"] > 10:
                current_text = "You cut through the vines."
            else:
                current_text = "The vines are too tough. You get tangled.\n\nLost 5 HP"
                character_statistics["HP"] -= 5
        elif choice == "Climb":
            if character_statistics["Dexterity"] > 10:
                current_text = "You climb over successfully."
            else:
                current_text = "You fall.\n\nLost 10 HP"
                character_statistics["HP"] -= 10
        elif choice == "Go Around":
            current_text = "You go around. It takes longer.\n\nLost 10 Energy"
            character_statistics["Energy"] -= 10
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_event20":
        if choice == "Find Shelter":
            if random.randint(1, 100) < 50:
                current_text = "You find shelter."
            else:
                current_text = "No shelter found.\n\nLost 10 HP"
                character_statistics["HP"] -= 10
        elif choice == "Run Through":
            if character_statistics["Speed"] > 15:
                current_text = "You run through safely."
            else:
                current_text = "You get lost in the storm.\n\nLost 15 HP"
                character_statistics["HP"] -= 15
        elif choice == "Wait":
            current_text = "You wait. The storm passes.\n\nLost 10 Energy"
            character_statistics["Energy"] -= 10
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_pirate_attack":
        if chosen_class == 1 or chosen_class == 3:  # Warrior or Defender
            if choice == "Board Boat":
                current_text = "You manage to lose the pirates for a short time, and sneak onto the boat, catching them completely by surprise. Because of your physical might, they don't stand a chance. The pirates are either slain or flee into the ocean to escape you. You continue your journey.\n\nGained 20 XP!"
                character_statistics["XP"] += 20
            elif choice == "Fire Cannon":
                current_text = "You have no cannon. The pirates do have a cannon. They shoot you.\n\nYou are slain."
                character_statistics["HP"] = 0
            elif choice == "Jump Water":
                if character_statistics["Swim"] > 10:
                    current_text = "You manage to jump into the water and hold your breath long enough while swimming away to lose the pirates. When you resurface, you find yourself somewhere completely new..."
                    teleport_random_biome()
                    return
                else:
                    fate = random.randint(1, 3)
                    if fate == 1:
                        current_text = "You are unable to swim well enough to save yourself from the pirates, but are caught up in a current and dragged hopelessly to safety. You are quite the lucky hero!"
                        teleport_random_biome()
                        return
                    elif fate == 2:
                        current_text = "It appears you have forgotten that you cannot swim very well, and swimming for miles is exhausting. You drown in the water."
                        character_statistics["HP"] = 0
                    else:
                        current_text = "You attempt to swim from the boat, but are far too slow to escape the pirates. You are captured."
                        current_event_name = "trigger_escape"
                        current_text, choices = trigger_escape()
                        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
                        current_event = handle_event_choice
                        return
        else:  # Mage
            if choice == "Board Boat":
                if character_statistics["Strength"] >= 10:
                    current_text = "You manage to lose the pirates for a short time, and sneak onto the boat, catching them completely by surprise. Because of your physical might, they don't stand a chance. The pirates are either slain or flee into the ocean to escape you. You continue your journey.\n\nGained 20 XP!"
                    character_statistics["XP"] += 20
                else:
                    fate = random.randint(1, 2)
                    if fate == 1:
                        if character_statistics["Magic"] >= 10:
                            current_text = "You board the boat, mindlessly firing fireballs in all directions. You manage to scare the pirates off, and take control of the ship.\n\nGained 20 XP"
                            character_statistics["XP"] += 20
                        else:
                            current_text = "You were not powerful enough to fight the pirates with your magical abilities, and you were slain. Rest in peace, great mage."
                            character_statistics["HP"] = 0
                    else:
                        current_text = "You foolishly attempt to attack the pirates using a sword, but you were not proficient enough. You are slain by the pirates."
                        character_statistics["HP"] = 0
            elif choice == "Magical Storm":
                if character_statistics["Magic"] > 5 and "Lightning Bolt" in current_spells:
                    current_text = "You conjure up an incredible storm using the power of the lightning bolt. You destroy the pirates, they won't be trying that again for a long time.\n\nGained 20 XP"
                    character_statistics["XP"] += 20
                elif character_statistics["Magic"] > 5:
                    current_text = "You conjure up a storm using your learned magical powers. The pirates retreat, but are not defeated.\n\nGained 5 XP"
                    character_statistics["XP"] += 5
                else:
                    current_text = "You must not have paid attention in wizarding school. You accidentally create an earthquake underneath yourself and are slain. Game over, great mage."
                    character_statistics["HP"] = 0
            elif choice == "Jump Water":
                if character_statistics["Swim"] > 10:
                    current_text = "You manage to jump into the water and hold your breath long enough while swimming away to lose the pirates. When you resurface, you find yourself somewhere completely new..."
                    teleport_random_biome()
                    return
                else:
                    fate = random.randint(1, 3)
                    if fate == 1:
                        current_text = "You are unable to swim well enough to save yourself from the pirates, but are caught up in a current and dragged hopelessly to safety. You are quite the lucky hero!"
                        teleport_random_biome()
                        return
                    elif fate == 2:
                        current_text = "It appears you have forgotten that you cannot swim very well, and swimming for miles is exhausting. You drown in the water."
                        character_statistics["HP"] = 0
                    else:
                        current_text = "You attempt to swim from the boat, but are far too slow to escape the pirates. You are captured."
                        current_event_name = "trigger_escape"
                        current_text, choices = trigger_escape()
                        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
                        current_event = handle_event_choice
                        return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_escape":
        if choice == "Loosen Bands":
            # Simplified: always succeed after a few attempts
            current_text = "After struggling with the bands, you manage to shake them off your wrists. What's next?"
            current_event_name = "trigger_escape2"
            current_text, choices = trigger_escape2()
            buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
            current_event = handle_event_choice
            return
        elif choice == "Call Help":
            current_text = "You shout for help, but all you can hear in response is your own echo."
            # Stay in same event
            return
        elif choice == "Create Light":
            if character_statistics["Magic"] > 3:
                current_text = "You struggle for a moment with the bands, but manage to create some light. There isn't much to take in, but you can tell you're in a prison cell.\n\nGained 2 Magic\nLost 5 Energy"
                character_statistics["Magic"] += 2
                character_statistics["Energy"] -= 5
                current_event_name = "trigger_escape3"
                current_text, choices = trigger_escape3()
                buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
                current_event = handle_event_choice
                return
            else:
                current_text = "You simply exhaust yourself trying to create magic. Who really believes in that stuff anyway?\n\nLost 10 Energy"
                character_statistics["Energy"] -= 10
                return
        # Stay in same event for stats/inventory
        return
    elif current_event_name == "trigger_escape2":
        if choice == "Blast Door":
            if character_statistics["Magic"] >= 5:
                if random.randint(1, 100) < 40:
                    current_text = "You burst through the door with a fireball, and rush out. Lucky for you, you broke out at night, and despite your very loud exit, nobody wakes up. You simply walk away, safe... for now."
                else:
                    current_text = "You bust out, and there are pirates guarding the door. You don't have much time, what do you do?"
                    buttons = [Button(50, 400, 100, 50, "Fight", PRIMARY_GREEN), Button(170, 400, 100, 50, "Run", PRIMARY_GREEN), Button(290, 400, 100, 50, "Surrender", PRIMARY_GREEN)]
                    current_event_name = "escape2_combat"
                    return
            else:
                current_text = "You don't have enough magic to blast through the door."
                return
        elif choice == "Sneak Out":
            current_text = "You try to sneak out quietly, but the door is locked. You need another approach."
            return
        elif choice == "Examine":
            current_text = "You examine your surroundings. You see a small window, some loose stones, and the door. The window might be climbable."
            return
        # Stay in same event for stats/inventory
        return
    elif current_event_name == "escape2_combat":
        if choice == "Fight":
            damage_taken = random.randint(2, 10)
            current_text = f"You fight through waves of pirates, and feel pretty cool doing so. You manage to get away from them and escape, but you notice a little late that you had been hurt...\n\nLost {damage_taken} HP\nGained 15 XP"
            character_statistics["HP"] -= damage_taken
            character_statistics["XP"] += 15
        elif choice == "Run":
            if character_statistics["Speed"] >= 5:
                if random.randint(1, 100) < 70:
                    current_text = "You run for your life, and don't stop until you stop hearing the footsteps following you. You turn around. You are safe... for now.\n\nGained 5 XP\nGained 1 Speed"
                    character_statistics["XP"] += 5
                    character_statistics["Speed"] += 1
                    teleport_random_biome()
                    buttons = [
                        Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                        Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                        Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                    ]
                    current_event = None
                    current_event_name = None
                    return
                elif random.randint(1, 100) < 85:
                    HP_lost = 10
                    if HP_lost >= character_statistics["HP"]:
                        HP_lost = character_statistics["HP"] - 1
                    current_text = f"You run and run, but suffer arrows in the back while attempting to escape. You survive, but don't feel so good...\n\nLost {HP_lost} HP\nGained 1 Speed"
                    character_statistics["HP"] -= HP_lost
                    character_statistics["Speed"] += 1
                    teleport_random_biome()
                    buttons = [
                        Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN),
                        Button(200, 400, 120, 50, "Stats", PRIMARY_BLUE),
                        Button(350, 400, 120, 50, "Inventory", PRIMARY_BLUE)
                    ]
                    current_event = None
                    current_event_name = None
                    return
                else:
                    current_text = "You try to run, but are immediately caught. The pirates are not merciful enough to put you back in your cell... You are slain."
                    character_statistics["HP"] = 0
            else:
                current_text = "You try to run but are too slow and get caught. You are slain."
                character_statistics["HP"] = 0
        elif choice == "Surrender":
            current_text = "You surrender and are thrown back in your cell. Better luck next time."
            current_event_name = "trigger_escape"
            current_text, choices = trigger_escape()
            buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
            current_event = handle_event_choice
            return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    elif current_event_name == "trigger_escape3":
        if choice == "Blast Door":
            if random.randint(1, 100) < character_statistics["Magic"] * 5:
                current_text = "You manage to blast the door down with a lightning bolt, and the subsequent burst of light stuns the pirates guarding the door. The pirates scramble to figure out what's going on, and you manage to slip away in the confusion."
                teleport_random_biome()
                return
            else:
                damage = character_statistics["Magic"]
                if damage >= character_statistics["HP"]:
                    damage = character_statistics["HP"] - 1
                current_text = f"You attempt to blow the door down, but accidentally summon a fireball too large, blasting the door down and slaying all pirates, but harming yourself in the process. After blacking out for a while, you awake to find yourself alone. You limp away, safe... for now.\n\nTook {damage} damage!"
                character_statistics["HP"] -= damage
                teleport_random_biome()
                return
        elif choice == "Forge Crowbar":
            if character_statistics["Magic"] >= 12:
                if random.randint(1, 100) < 60:
                    current_text = "You manage to form the pebbles into a crowbar using your magic. It drains your energy, but you manage to escape by using it to crawl through the window and sneak away. Unfortunately, you forgot to bring the crowbar with you. Oh well.\n\nLost 20 Energy"
                    character_statistics["Energy"] -= 20
                    teleport_random_biome()
                    return
                else:
                    if random.randint(1, 100) < character_statistics["Speed"] * 5:
                        current_text = "You manage to forge a crowbar using magic, but while trying to sneak out, you are seen by the guards and attempt to flee. You successfully make your getaway, and feel pretty good afterwards!\n\nGained 1 Speed\nGained 5 Energy"
                        character_statistics["Speed"] += 1
                        character_statistics["Energy"] += 5
                        teleport_random_biome()
                        return
                    else:
                        current_text = "You manage to forge a crowbar using magic, but while trying to sneak out, you are seen by the guards and attempt to flee. Unfortunately, you were too slow and are forced to fight, leaving you badly wounded, but alive. You escape.\n\nDown to 1 HP!"
                        character_statistics["HP"] = 1
                        teleport_random_biome()
                        return
            else:
                current_text = "You cannot create a crowbar with your current magic level."
                return
        elif choice == "Bucket Head":
            if random.randint(1, 100) < 99:
                current_text = "Well done. Now you cannot see and look like a fool. What did you expect to happen?\n\nLost 5 Morale"
                character_statistics["Morale"] -= 5
            else:
                current_text = "You place the bucket on your head at the exact moment a pirate happens to walk in. He must be blind, because he couldn't see you and left the door open behind him. You quietly sneak out and nobody bats an eye. How nice!"
                teleport_random_biome()
                return
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return
    else:
        # Default handler for unimplemented events
        current_text = f"You encounter an event ({current_event_name}), but this event is not yet fully implemented. You continue on your journey."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        current_event_name = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
        return

def handle_shop_choice(choice):
    global current_text, buttons, current_event, inventory
    
    if choice == "Purchase":
        current_text = "What would you like to purchase?\nWood: 2 gold each\nIron: 3 gold each\nGold: 5 gold each\nYou have " + str(inventory['Money']) + " gold."
        buttons = [
            Button(50, 400, 100, 50, "Wood", PRIMARY_GREEN),
            Button(170, 400, 100, 50, "Iron", PRIMARY_GREEN),
            Button(290, 400, 100, 50, "Gold", PRIMARY_GREEN),
            Button(410, 400, 100, 50, "Back", RED)
        ]
        current_event = handle_purchase_choice
    elif choice == "Sell":
        current_text = "What would you like to sell?\nWood: 1 gold each\nIron: 2 gold each\nGold: 3 gold each"
        buttons = [
            Button(50, 400, 100, 50, "Wood", PRIMARY_GREEN),
            Button(170, 400, 100, 50, "Iron", PRIMARY_GREEN),
            Button(290, 400, 100, 50, "Gold", PRIMARY_GREEN),
            Button(410, 400, 100, 50, "Back", RED)
        ]
        current_event = handle_sell_choice
    elif choice == "Leave":
        current_text = "You leave the shop and continue your journey."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()
    elif choice in ["Stats", "Inventory"]:
        if choice == "Stats":
            # Open profile.html in browser
            profile_path = os.path.join(os.path.dirname(__file__), "profile.html")
            webbrowser.open(f"file://{profile_path}")
        elif choice == "Inventory":
            # Open inventory.html in browser
            inventory_path = os.path.join(os.path.dirname(__file__), "inventory.html")
            webbrowser.open(f"file://{inventory_path}")
        return

def handle_purchase_choice(choice):
    global current_text, buttons, current_event, inventory
    
    if choice == "Back":
        current_text, choices = trigger_shop()
        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < 3 else PRIMARY_BLUE) for i, c in enumerate(choices)]
        current_event = handle_shop_choice
        return
    
    prices = {"Wood": 2, "Iron": 3, "Gold": 5}
    if choice in prices:
        price = prices[choice]
        if inventory['Money'] >= price:
            inventory['Money'] -= price
            inventory[choice] += 1
            current_text = f"You purchased 1 {choice} for {price} gold. You have {inventory['Money']} gold left."
        else:
            current_text = f"You don't have enough gold to purchase {choice}."
    else:
        current_text = "Invalid choice."
    
    buttons = [Button(50, 400, 120, 50, "Continue Shopping", PRIMARY_GREEN), Button(200, 400, 120, 50, "Leave Shop", RED)]
    current_event = handle_purchase_continue

def handle_purchase_continue(choice):
    global current_text, buttons, current_event
    
    if choice == "Continue Shopping":
        current_text, choices = trigger_shop()
        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < 3 else PRIMARY_BLUE) for i, c in enumerate(choices)]
        current_event = handle_shop_choice
    elif choice == "Leave Shop":
        current_text = "You leave the shop and continue your journey."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()

def handle_sell_choice(choice):
    global current_text, buttons, current_event, inventory
    
    if choice == "Back":
        current_text, choices = trigger_shop()
        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < 3 else PRIMARY_BLUE) for i, c in enumerate(choices)]
        current_event = handle_shop_choice
        return
    
    sell_prices = {"Wood": 1, "Iron": 2, "Gold": 3}
    if choice in sell_prices and inventory[choice] > 0:
        price = sell_prices[choice]
        inventory[choice] -= 1
        inventory['Money'] += price
        current_text = f"You sold 1 {choice} for {price} gold. You have {inventory['Money']} gold now."
    else:
        current_text = f"You don't have any {choice} to sell."
    
    buttons = [Button(50, 400, 120, 50, "Continue Selling", PRIMARY_GREEN), Button(200, 400, 120, 50, "Leave Shop", RED)]
    current_event = handle_sell_continue

def handle_sell_continue(choice):
    global current_text, buttons, current_event
    
    if choice == "Continue Selling":
        current_text, choices = trigger_shop()
        buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < 3 else PRIMARY_BLUE) for i, c in enumerate(choices)]
        current_event = handle_shop_choice
    elif choice == "Leave Shop":
        current_text = "You leave the shop and continue your journey."
        buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        current_event = None
        game_over = does_game_end()
        if game_over:
            current_text = game_over
            buttons = []
            return
        level_up()

def print_choices(choice_list):
    return choice_list

def print_stats():
    stats = "\n".join([f"{k}: {v}" for k, v in character_statistics.items()])
    return stats

def check_inventory():
    inv = "\n".join([f"{k}: {v}" for k, v in inventory.items()])
    return inv

def print_enemy_stats():
    enemy = "\n".join([f"{k}: {v}" for k, v in enemy_stats.items()])
    return enemy

def all_stats_increase():
    character_statistics["Defence"] += 1
    character_statistics["Strength"] += 1
    character_statistics["Magic"] += 1
    character_statistics["Dexterity"] += 1
    character_statistics["Swim"] += 1
    character_statistics["Speed"] += 1
    character_statistics["Intellect"] += 1

def level_up():
    global max_HP
    global max_Mana

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
        OldHP = max_HP
        OldLevel = character_statistics["Level"]
        OldStrength = character_statistics["Strength"]
        OldMagic = character_statistics["Magic"]
        OldDefense = character_statistics["Defense"]
        OldSwim = character_statistics["Swim"]
        OldSpeed = character_statistics["Speed"]
        OldMana = max_Mana
        OldDexterity = character_statistics["Dexterity"]
        OldIntellect = character_statistics["Intellect"]

        # Spend XP & level up first
        required_XP = character_statistics["Level"] * math.ceil(10 * character_statistics["Level"])
        character_statistics["XP"] -= required_XP
        character_statistics["Level"] += 1

        # Preferred stat bonus (always at least +1)
        character_statistics[preferred_stat] += random.randint(1, math.ceil(character_statistics[preferred_stat] * 0.25))

        # Bonus stats depending on level
        if character_statistics["Level"] % 1 == 0:
            max_Mana += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
            max_HP += random.randint(1, 2)
            character_statistics["Mana"] = max_Mana
            character_statistics["HP"] = max_HP
        if character_statistics["Level"] % 2 == 0:
            character_statistics["Strength"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))
            character_statistics["Speed"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
            character_statistics["Dexterity"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
        if character_statistics["Level"] % 3 == 0:
            character_statistics["Magic"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))
            character_statistics["Swim"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.5))
            character_statistics["Intellect"] += random.randint(1, math.ceil(character_statistics["Level"] * 0.75))
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
        level_text = f"""
        LEVEL UP!
   Level: {OldLevel} ---> {character_statistics["Level"]}
   HP: {OldHP} ---> {max_HP}
   Mana: {OldMana} ---> {max_Mana}
Strength: {OldStrength} ---> {character_statistics["Strength"]}
 Defense: {OldDefense} ---> {character_statistics["Defense"]}
   Magic: {OldMagic} ---> {character_statistics["Magic"]}
   Speed: {OldSpeed} ---> {character_statistics["Speed"]}
    Swim: {OldSwim} ---> {character_statistics["Swim"]}
    Dexterity: {OldDexterity} ---> {character_statistics["Dexterity"]}
    Intellect: {OldIntellect} ---> {character_statistics["Intellect"]}"""
        return level_text

def does_game_end():
    # check if game ends
    if character_statistics["HP"] <= 0:
        return "You take too much damage, and are unable to continue. Game Over."
    elif character_statistics["Morale"] <= 0:
        return "Your morale has reached the lowest of lows. Maybe this whole adventuring thing isn't really for you. You give up."
    elif character_statistics["Energy"] <= 0:
        return "You collapse from exhaustion. Game Over."

    # check stats overflow and reset
    if character_statistics["HP"] > max_HP:
        character_statistics["HP"] = max_HP
    elif character_statistics["Morale"] > 100:
        character_statistics["Morale"] = 100
    elif character_statistics["Energy"] > 100:
        character_statistics["Energy"] = 100
    else:
        return None

def teleport_random_biome():
    global Csetting, current_biome
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
    current_biome = Csetting
    text = f"You have arrived in the {Csetting}."
    return text

def enter_setting(NewSetting):
    global Csetting, current_biome
    setting[Csetting] = False
    Csetting = NewSetting
    setting[Csetting] = True
    current_biome = Csetting
    text = f"You have arrived in the {Csetting}."
    return text

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
        return "Your attack missed!"
    if attack_type.lower() == "melee":
        damage_dealt = ((character_statistics["Strength"] * 0.25) * weapon_damage) - enemy_stats["Defense"]
    elif attack_type.lower() == "magic":
        damage_dealt = ((character_statistics["Magic"] * 0.35) * weapon_damage) - enemy_stats["Magic"]
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
        enemy_stats["HP"] -= (2*damage_dealt)
        return f"Critical hit! You dealt {math.ceil(2*damage_dealt)} damage."
    else:
        enemy_stats["HP"] -= math.ceil(damage_dealt)
        return f"You dealt {math.ceil(damage_dealt)} damage."

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
        return "Invalid choice — not a number."

    if choice == 1:
        return

    if choice in item_lookup:
        item = item_lookup[choice]
        if item.lower() == "wood":
            return ""
        elif item.lower() == "gold":
            # Throw gold at enemy
            if random.randint(1, 50) < character_statistics["Dexterity"] * character_statistics["Strength"] + 5:
                damage = calculate_damage("throw", random.randint(1, 10), 1)
                return f"You chuck a piece of gold at the enemy, dealing {damage} damage"
            else:
                return "You throw the gold at the enemy, but you completely miss."
        elif item.lower() == "rubber ducks":
            return "Quack! Rubber ducks selected"
    else:
        return "Invalid choice — number not in menu."

def is_valid_weapon(choice):
    choice = choice.strip().title()

    weapon_stats = weapons.get(choice)
    if not weapon_stats:
        return "Invalid weapon! (GAME BUG)"

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
        text = f"You attack with your {choice} dealing {damage} damage. The enemy has {enemy_stats['HP']} HP left."
    else:
        text = f"You attack with your {choice} dealing {damage} damage. The enemy has been slain."

    # Handle special power (if any)
    if weapon_stats.get("special_power") and weapon_stats["special_power"] != "none":
        text += f"The {choice} unleashes its special power: {weapon_stats['special_power'].capitalize()}!"
        special_power(weapon_stats['special_power'].lower())

    return text

def is_valid_spell(choice):
    choice = choice.strip().title()

    spell_stats = spells.get(choice)
    if not spell_stats:
        return "Invalid spell! (GAME BUG)"

    # Calculate damage
    damage = calculate_damage("magic",spell_stats["damage"],spell_stats["hit_chance"])
    character_statistics["Mana"] -= spell_stats["mana_cost"]
    if damage is None:
        return

    # Print attack message
    if enemy_stats["HP"] >= 0:
        text = f"You attack with your {choice} dealing {damage} damage. The enemy has {enemy_stats['HP']} HP left."
    else:
        text = f"You attack with your {choice} dealing {damage} damage. The enemy has been slain."

    # Handle special power (if any)
    if spell_stats.get("special_power") and spell_stats["special_power"] != "none":
        text += f"The {choice} unleashes its special power: {spell_stats['special_power'].capitalize()}!"
        special_power(spell_stats['special_power'].lower())

    return text

def special_power(power):
    if power == "fire":
        return "The enemy is burning."

def enemy_dead(combat_opponent, enemy_level):
    if combat_opponent.lower() == "hydra":
        xp = enemy_level * math.ceil(random.randint(10, 20))
        character_statistics["XP"] += xp
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "goblin":
        xp = enemy_level * math.ceil(random.randint(1, 3))
        character_statistics["XP"] += xp
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "ogre":
        xp = enemy_level * math.ceil(random.randint(2, 5))
        character_statistics["XP"] += xp
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "orc":
        xp = enemy_level * math.ceil(random.randint(4, 7))
        character_statistics["XP"] += xp
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "wizard":
        xp = enemy_level * math.ceil(random.randint(5, 8))
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "bandit":
        xp = enemy_level * math.ceil(random.randint(3, 5))
        return f"Gained {xp} XP"
    elif combat_opponent.lower() == "dragon":
        xp = enemy_level * math.ceil(random.randint(12, 18))
        return f"Gained {xp} XP"
    else:
        return

# Set enemy stats
def trigger_battle(combat_opponent, enemy_level):
    # Optional ability for random battle opponent
    import random

    enemies = {
        "hydra": {"encounter_chance": 10},
        "goblin": {"encounter_chance": 40},
        "orc": {"encounter_chance": 20},
        "ogre": {"encounter_chance": 20},
        "wizard": {"encounter_chance": 15},
        "golem": {"encounter_chance": 15},
        "dragon": {"encounter_chance": 5},
        "bandit": {"encounter_chance": 40},
        "troll": {"encounter_chance": 20}
    }

    opponents = list(enemies.keys())
    encounter_chance = [enemies[o]["encounter_chance"] for o in opponents]
    combat_opponent = random.choices(opponents, weights=encounter_chance, k=1)[0]

    # Ensure Enemy isn't too powerful or too weak

    if enemy_level == 0:
        enemy_level = random.randint(math.ceil(.75 * character_statistics["Level"]), math.ceil(1.5 * character_statistics["Level"]))
    else:
        enemy_level = random.randint(1, 1000)
        for i in range(20):
            new_level = random.randint(1, 1000)
            if enemy_level > new_level:
                new_level = enemy_level
        enemy_level = new_level
    if enemy_level > math.ceil(1.5 * character_statistics["Level"]):
        enemy_level = math.ceil(1.5 * character_statistics["Level"])
    if enemy_level < math.ceil(.75 * character_statistics["Level"]):
        enemy_level = math.ceil(.75 * character_statistics["Level"])

    # Hydra Battle
    if combat_opponent.lower() == "hydra":
        text = f"You are in combat against a level {enemy_level} hydra."
        enemy_stats["HP"] = 100 * enemy_level
        enemy_stats["Strength"] = 5 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Goblin Battle
    elif combat_opponent.lower() == "goblin":
        text = f"You are in combat against a level {enemy_level} goblin."
        enemy_stats["HP"] =  30 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Ogre Battle
    elif combat_opponent.lower() == "ogre":
        text = f"You are in combat against a level {enemy_level} ogre."
        enemy_stats["HP"] =  60 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Orc Battle
    elif combat_opponent.lower() == "orc":
        text = f"You are in combat against a level {enemy_level} orc."
        enemy_stats["HP"] =  80 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 5 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Wizard Battle
        text = f"You are in combat against a level {enemy_level} wizard."
        enemy_stats["HP"] =  50 * enemy_level
        enemy_stats["Strength"] = 0
        enemy_stats["Defense"] = 1 * enemy_level
        enemy_stats["Speed"] = 3 * enemy_level
        enemy_stats["Magic"] = 4 * enemy_level

    # Golem Battle
        text = f"You are in combat against a level {enemy_level} golem."
        enemy_stats["HP"] =  110 * enemy_level
        enemy_stats["Strength"] = 2 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 1 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Bandit Battle
    elif combat_opponent.lower() == "bandit":
        text = f"You are in combat against a level {enemy_level} bandit."
        enemy_stats["HP"] =  40 * enemy_level
        enemy_stats["Strength"] = 3 * enemy_level
        enemy_stats["Defense"] = 2 * enemy_level
        enemy_stats["Speed"] = 6 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    # Dragon Battle
    elif combat_opponent.lower() == "dragon":
        text = f"You are in combat against a level {enemy_level} dragon."
        enemy_stats["HP"] =  150 * enemy_level
        enemy_stats["Strength"] = 6 * enemy_level
        enemy_stats["Defense"] = 8 * enemy_level
        enemy_stats["Speed"] = 5 * enemy_level
        enemy_stats["Magic"] = 5 * enemy_level

    elif combat_opponent.lower() == "troll":
    # Troll Battle
        text = f"You are in combat against a level {enemy_level} troll."
        enemy_stats["HP"] =  60 * enemy_level
        enemy_stats["Strength"] = 8 * enemy_level
        enemy_stats["Defense"] = 4 * enemy_level
        enemy_stats["Speed"] = 2 * enemy_level
        enemy_stats["Magic"] = 1 * enemy_level

    else:
        text = "ERROR: No valid enemy selected"
        return text, ["Continue"]
    
    return text, ["Attack", "Use Spell", "Use Item", "Flee", "Inventory", "Stats", "Enemy Stats"], combat_opponent, enemy_level

def combat_attack():
    global current_text
    while enemy_stats["HP"] > 0:
        if(random.randint(1, 100) < 90):
            choices = ["Use Weapon", "Use Spell", "Use Item", "Flee", "Inventory", "Stats", "Enemy Stats"]
            return "You manage to get a jump on the opponent, what do you do?", choices
        else:
            return combat_defense("melee" if enemy_stats["Strength"] >= enemy_stats["Magic"] else "magic")

def combat_defense(attack_type):
    choices = ["Block", "Dodge", "Flee", "Inventory", "Stats", "Enemy Stats"]
    return "The opponent manages to get a jump on you, how do you protect yourself?", choices, attack_type

def calculate_player_damage(is_blocking, attack_type):
    # Enemy attacks with melee
    if is_hit(100 - 10*character_statistics["Speed"]) == False:
        return "The enemy attack missed!"
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
    return f"Took {damage_dealt} damage! You have {character_statistics['HP']} HP left."

def show_weapon(name, stats):
    return f"Weapon Get!\n{name} | {stats['rarity']}\n{stats['damage']} Damage\n{stats['hit_chance']} Hit chance"

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
        return show_weapon(weapon_name, stats)
    else:
        # Otherwise, ask the player if they want to replace something
        return show_weapon(weapon_name, stats), ["Take", "Leave"], weapon_name

# Template for building events
def trigger_event_0():
    choices = ["Option 1", "Option 2", "Option 3", "Stats", "Inventory"]
    return "Template Event\n1. \n2. \n3. \n4. Stats\n5. Inventory", choices

# All Game Events

def trigger_pirate_attack():
    if chosen_class == 1 or chosen_class == 3:
        text = "You engage in combat with the pirates!\n1. Attempt to board and steal pirate boat\n2. Fire a cannon at the enemy boat\n3. Jump into the water for safety\n4. Stats\n5. Inventory"
        choices = ["Board Boat", "Fire Cannon", "Jump in Water", "Stats", "Inventory"]
    else:
        text = "You engage in combat with the pirates!\n1. Attempt to board and steal pirate boat\n2. Conjure a magical storm to destroy the pirates\n3. Jump into the water for safety\n4. Stats\n5. Inventory"
        choices = ["Board Boat", "Conjure Storm", "Jump in Water", "Stats", "Inventory"]
    return text, choices

def trigger_escape():
    text = "You awake, tied up in the dark. You have been captured, and need to find a way to escape. What do you do?\n1. Attempt to loosen the bands\n2. Call out for help\n3. Create magical light\n4. Stats\n5. Inventory"
    choices = ["Loosen Bands", "Call Help", "Magical Light", "Stats", "Inventory"]
    return text, choices

def trigger_escape2():
    text = "It's still pitch black, but at least you aren't shackled anymore. What is your escape plan?\n1. Blast through the door\n2. Sneak out\n3. Examine your surroundings\n4. Stats\n5. Inventory"
    choices = ["Blast Door", "Sneak Out", "Examine", "Stats", "Inventory"]
    return text, choices

def trigger_escape3():
    text = "Now that you have a better idea of what's going on, you need to think of a way to escape. You slip out of your restraints, and in the room you see a door, a boarded window, a bucket, a few pebbles and a stick. How do you escape?\n1. Use magic to blast the door down\n2. Forge a crowbar from the pebbles and sneak out the window\n3. Place the bucket on your head.\n4. Stats\n5. Inventory"
    choices = ["Blast Door", "Forge Crowbar", "Bucket on Head", "Stats", "Inventory"]
    return text, choices

# Any Biome
def trigger_shop():
    text = f"You come across a vendor during your travels. \"I've got wares, why don't you take a look?\" He suspiciously says. You've got {inventory['Money']} money\n1. Purchase\n2. Sell\n3. Leave\n4. Stats\n5. Inventory"
    choices = ["Purchase", "Sell", "Leave", "Stats", "Inventory"]
    return text, choices

# Starting Event
def trigger_event1():
    text = "A challenger stands before you: a simple goblin. What will you do fighter?\n1. Attack with the sword\n2. Strike him with a fireball\n3. Run for your pitiful little life\n4. Stats\n5. Inventory"
    choices = ["Attack Sword", "Fireball", "Run", "Stats", "Inventory"]
    return text, choices

# Swamp Event
def trigger_event2():
    text = "Another challenge awaits! You find yourself in a thick swamp. What will you do?\n1. Scavenge for resources\n2. Explore further\n3. Rest yourself\n4. Stats\n5. Inventory"
    choices = ["Scavenge for resources", "Explore further", "Rest yourself", "Stats", "Inventory"]
    return text, choices

# Forest Event
def trigger_event3():
    text = "While stumbling across the forest, you are ambushed by a group of gnomes. What will you do?\n1. Attempt a spin attack with your sword\n2. Cast a lightning strike to destroy the ambush\n3. Attempt to bribe the gnomes\n4. Stats\n5. Inventory"
    choices = ["Spin Attack", "Lightning Strike", "Bribe", "Stats", "Inventory"]
    return text, choices

# Tundra Event
def trigger_event4():
    text = "You come across an igloo in the snow covered landscape. You walk inside. What do you do there?\n1. Take a nap\n2. Melt the igloo to search for more goods\n3. Take an icicle bolt spell book from the wall\n4. Stats\n5. Inventory"
    choices = ["Nap", "Melt Igloo", "Take Book", "Stats", "Inventory"]
    return text, choices

# Swamp Event
def trigger_event5():
    text = "As you wander throughout the swamp, confused and lost, you encounter an old witch. She invites you to come inside and try a potion. What will you do?\n1. Drink the potion the witch gives you\n2. Slay the witch\n3. Run away\n4. Stats\n5. Inventory"
    choices = ["Drink Potion", "Slay Witch", "Run Away", "Stats", "Inventory"]
    return text, choices

# Swamp Event
def trigger_event6():
    text = "While sloshing through some mud, you feel something rubbing against your foot. What will you do?\n1. Reach down and grab the thing rubbing against you\n2. Attempt to clear the mud by digging really fast to get a better look\n3. Ignore whatever it was and keep sloshing around\n4. Stats\n5. Inventory"
    choices = ["Grab", "Dig", "Ignore", "Stats", "Inventory"]
    return text, choices

def trigger_event6_enemy():
    text = "Oh no! It's a shark... Your worst nightmare! How will you rid of this foe?\n1. Bite it!\n2. Blast it with a fireball\n3. Swim as fast as you can\n4. Stats\n5. Inventory"
    choices = ["Bite", "Fireball", "Swim", "Stats", "Inventory"]
    return text, choices

# Forest Event
def trigger_event7():
    text = "You encounter a wizard deep in the forest. He appears to be nice! He hands you a book. What a nice guy.\nObtain Lightning Bolt"
    choices = ["Continue"]
    return text, choices

# Plains/Forest/Jungle Event
def trigger_event8():
    text = "You come across an ocean. What will you do?\n1. Go fishing and relax\n2. Turn around and ignore it\n3. Build a boat and sail the seas\n4. Stats\n5. Inventory"
    choices = ["Fish", "Ignore", "Build Boat", "Stats", "Inventory"]
    return text, choices

# Tundra Event
def trigger_event9():
    text = "While travelling through the tundra, you come across a large, icy river, filled to the brim with hungry and violent fish. What will you do?\n1. Attempt to slay the fish for food\n2. Run through the icy river\n3. Build a bridge to cross the river\n4. Stats\n5. Inventory"
    choices = ["Slay Fish", "Run Through", "Build Bridge", "Stats", "Inventory"]
    return text, choices

# Plains Event
def trigger_event10():
    text = "You discover the fountain of youth while wandering through the plains. What do you do?\n1. Enter the fountain\n2. Have a refreshing drink\n3. Store some for later\n4. Stats\n5. Inventory"
    choices = ["Enter", "Drink", "Store", "Stats", "Inventory"]
    return text, choices

# Side Event
def trigger_event10_1():
    text = "What do you do?\n1. Attack the monster\n2. Comply with the monster\n3. Ignore the monster\n4. Stats\n5. Inventory"
    choices = ["Attack", "Comply", "Ignore", "Stats", "Inventory"]
    return text, choices

# Forest Event
def trigger_event11():
    text = "You take an arrow to the knee. Ow.\n1. Pull it out\n2. Break off the end of it\n3. Leave it\n4. Stats\n5. Inventory"
    choices = ["Pull Out", "Break Off", "Leave", "Stats", "Inventory"]
    return text, choices

# Mountain Event
def trigger_event12():
    text = "You stumble upon a bridge whilst adventuring through the mountains, and are encountered by an old man. He tells you something about answering 3 questions correctly to cross the bridge, and otherwise you'll die. What do you do?\n1. Answer him these questions 3\n2. Cross the bridge without answering the questions\n3. Turn and run\n4. Stats\n5. Inventory"
    choices = ["Answer Questions", "Cross Bridge", "Run", "Stats", "Inventory"]
    return text, choices

def trigger_event12_1():
    question = random.randint(1, 5)
    if question == 1:
        text = "What... is your name?"
        return text, ["Answer"]
    if question == 2:
        if random.randint(1, 100) < 30:
            text = "What... is your favorite color?"
            return text, ["Answer"]
        else:
            text = "What... is your favorite color?"
            return text, ["Answer"]
    if question == 3:
        text = "What... is the airspeed velocity of an unladen swallow?"
        return text, ["Answer"]
    elif question == 4:
        text = "In the works"
        return text, ["Continue"]
    elif question == 5:
        text = "In the works"
        return text, ["Continue"]

# Desert Event
def trigger_event13():
    text = "The desert is hot. You haven't had anything to drink in days. Suddenly, you see an oasis in the distance. You are saved!\n1. Go to the oasis and have a drink\n2. Ignore it and keep going\n3. Collapse and hope someone finds you\n4. Stats\n5. Inventory"
    choices = ["Drink", "Ignore", "Collapse", "Stats", "Inventory"]
    return text, choices

# Forest Event - Friendly Animal
def trigger_event14():
    text = "You hear rustling in the bushes. A friendly deer appears!\n1. Try to pet it\n2. Hunt it for food\n3. Ignore it and continue\n4. Stats\n5. Inventory"
    choices = ["Pet", "Hunt", "Ignore", "Stats", "Inventory"]
    return text, choices

# Swamp Event - Poisonous Plants
def trigger_event15():
    text = "You see glowing plants in the swamp. They look dangerous.\n1. Touch them\n2. Avoid them\n3. Try to harvest them\n4. Stats\n5. Inventory"
    choices = ["Touch", "Avoid", "Harvest", "Stats", "Inventory"]
    return text, choices

# Plains Event - Herd of Animals
def trigger_event16():
    text = "A herd of wild horses runs across the plains.\n1. Try to tame one\n2. Scare them away\n3. Watch them pass\n4. Stats\n5. Inventory"
    choices = ["Tame", "Scare", "Watch", "Stats", "Inventory"]
    return text, choices

# Ocean Event - Sea Monster
def trigger_event17():
    text = "A sea monster emerges from the depths!\n1. Fight it\n2. Dive underwater to hide\n3. Sail away\n4. Stats\n5. Inventory"
    choices = ["Fight", "Dive", "Sail", "Stats", "Inventory"]
    return text, choices

# Tundra Event - Blizzard
def trigger_event18():
    text = "A blizzard hits! You need shelter.\n1. Build a snow fort\n2. Keep moving\n3. Find a cave\n4. Stats\n5. Inventory"
    choices = ["Build Fort", "Keep Moving", "Find Cave", "Stats", "Inventory"]
    return text, choices

# Jungle Event - Vines
def trigger_event19():
    text = "Thick vines block your path in the jungle.\n1. Cut them\n2. Climb over\n3. Go around\n4. Stats\n5. Inventory"
    choices = ["Cut", "Climb", "Go Around", "Stats", "Inventory"]
    return text, choices

# Desert Event - Sandstorm
def trigger_event20():
    text = "A sandstorm approaches!\n1. Find shelter\n2. Run through it\n3. Wait it out\n4. Stats\n5. Inventory"
    choices = ["Find Shelter", "Run Through", "Wait", "Stats", "Inventory"]
    return text, choices

# Mountains Event - Avalanche
def trigger_event21():
    text = "You hear rumbling. An avalanche is coming!\n1. Climb higher\n2. Hide behind rocks\n3. Run downhill\n4. Stats\n5. Inventory"
    choices = ["Climb", "Hide", "Run", "Stats", "Inventory"]
    return text, choices

# Forest Event - Treasure Chest
def trigger_event22():
    text = "You find a chest hidden in the forest.\n1. Open it\n2. Check for traps\n3. Leave it\n4. Stats\n5. Inventory"
    choices = ["Open", "Check Traps", "Leave", "Stats", "Inventory"]
    return text, choices

# Swamp Event - Quicksand
def trigger_event23():
    text = "You step into quicksand!\n1. Struggle\n2. Use a rope (if you have one)\n3. Call for help\n4. Stats\n5. Inventory"
    choices = ["Struggle", "Use Rope", "Call Help", "Stats", "Inventory"]
    return text, choices

# Forest Event - Ancient Ruins
def trigger_event24():
    text = "You stumble upon ancient ruins in the forest.\n1. Enter the ruins\n2. Search the perimeter\n3. Leave\n4. Stats\n5. Inventory"
    choices = ["Enter", "Search", "Leave", "Stats", "Inventory"]
    return text, choices

# Swamp Event - Foggy Mystery
def trigger_event25():
    text = "A thick fog rolls in over the swamp.\n1. Navigate through the fog\n2. Wait for it to clear\n3. Build a signal fire\n4. Stats\n5. Inventory"
    choices = ["Navigate", "Wait", "Build Fire", "Stats", "Inventory"]
    return text, choices

# Plains Event - River Crossing
def trigger_event26():
    text = "A wide river blocks your path on the plains.\n1. Swim across\n2. Build a raft\n3. Find a bridge\n4. Stats\n5. Inventory"
    choices = ["Swim", "Build Raft", "Find Bridge", "Stats", "Inventory"]
    return text, choices

# Ocean Event - Island Discovery
def trigger_event27():
    text = "You spot an island in the distance.\n1. Sail to it\n2. Ignore it\n3. Send a scout\n4. Stats\n5. Inventory"
    choices = ["Sail", "Ignore", "Scout", "Stats", "Inventory"]
    return text, choices

# Tundra Event - Ice Cave
def trigger_event28():
    text = "You find an ice cave entrance.\n1. Enter\n2. Mine ice\n3. Seal it\n4. Stats\n5. Inventory"
    choices = ["Enter", "Mine", "Seal", "Stats", "Inventory"]
    return text, choices

# Jungle Event - Tribal Encounter
def trigger_event29():
    text = "Jungle tribesmen approach.\n1. Trade\n2. Fight\n3. Hide\n4. Stats\n5. Inventory"
    choices = ["Trade", "Fight", "Hide", "Stats", "Inventory"]
    return text, choices

# Desert Event - Caravan
def trigger_event30():
    text = "A desert caravan is stranded.\n1. Help them\n2. Rob them\n3. Ignore\n4. Stats\n5. Inventory"
    choices = ["Help", "Rob", "Ignore", "Stats", "Inventory"]
    return text, choices

# Mountains Event - Summit View
def trigger_event31():
    text = "From the mountain summit, you see...\n1. A valley\n2. Another peak\n3. Descend\n4. Stats\n5. Inventory"
    choices = ["Valley", "Peak", "Descend", "Stats", "Inventory"]
    return text, choices

# Forest Event - Mushroom Circle
def trigger_event32():
    text = "A circle of glowing mushrooms.\n1. Eat one\n2. Study them\n3. Destroy\n4. Stats\n5. Inventory"
    choices = ["Eat", "Study", "Destroy", "Stats", "Inventory"]
    return text, choices

# Plains Event - Abandoned Farm
def trigger_event33():
    text = "An abandoned farm.\n1. Search house\n2. Check barn\n3. Rest\n4. Stats\n5. Inventory"
    choices = ["Search House", "Check Barn", "Rest", "Stats", "Inventory"]
    return text, choices

# Pirate Attack Sequence
def trigger_pirate_attack():
    global current_text, buttons, current_event_name
    if chosen_class == 1 or chosen_class == 3:  # Warrior or Defender
        text = "You engage in combat with the pirates!\n1. Attempt to board and steal pirate boat\n2. Fire a cannon at the enemy boat\n3. Jump into the water for safety\n4. Stats\n5. Inventory"
        choices = ["Board Boat", "Fire Cannon", "Jump Water", "Stats", "Inventory"]
    else:  # Mage
        text = "You engage in combat with the pirates!\n1. Attempt to board and steal pirate boat\n2. Conjure a magical storm to destroy the pirates\n3. Jump into the water for safety\n4. Stats\n5. Inventory"
        choices = ["Board Boat", "Magical Storm", "Jump Water", "Stats", "Inventory"]
    return text, choices

# Escape Sequence 1 (Initial capture)
def trigger_escape():
    text = "You awake, tied up in the dark. You have been captured, and need to find a way to escape. What do you do?\n1. Attempt to loosen the bands\n2. Call out for help\n3. Create magical light\n4. Stats\n5. Inventory"
    choices = ["Loosen Bands", "Call Help", "Create Light", "Stats", "Inventory"]
    return text, choices

# Escape Sequence 2 (After loosening bands)
def trigger_escape2():
    text = "It's still pitch black, but at least you aren't shackled anymore. What is your escape plan?\n1. Blast through the door\n2. Sneak out\n3. Examine your surroundings\n4. Stats\n5. Inventory"
    choices = ["Blast Door", "Sneak Out", "Examine", "Stats", "Inventory"]
    return text, choices

# Escape Sequence 3 (With light)
def trigger_escape3():
    text = "Now that you have a better idea of what's going on, you need to think of a way to escape. You slip out of your restraints, and in the room you see a door, a boarded window, a bucket, a few pebbles and a stick. How do you escape?\n1. Use magic to blast the door down\n2. Forge a crowbar from the pebbles and sneak out the window\n3. Place the bucket on your head\n4. Stats\n5. Inventory"
    choices = ["Blast Door", "Forge Crowbar", "Bucket Head", "Stats", "Inventory"]
    return text, choices

def trigger_random_event():
    global current_text, buttons, current_event, current_event_name
    
    # List of available events for the current biome
    if setting["Forest"] == True:
        forest_events = [
            trigger_event2, trigger_event7, trigger_event8, trigger_event14, 
            trigger_event22, trigger_event24, trigger_event7, trigger_event8, 
            trigger_event14, trigger_event32
        ]
        selected_event = random.choice(forest_events)
    elif setting["Swamp"] == True:
        swamp_events = [
            trigger_event2, trigger_event5, trigger_event2, trigger_event5, 
            trigger_event5, trigger_event5, trigger_event5, trigger_event6, 
            trigger_event15, trigger_event25
        ]
        selected_event = random.choice(swamp_events)
    elif setting["Tundra"] == True:
        tundra_events = [
            trigger_event4, trigger_event4, trigger_event4, trigger_event9, 
            trigger_event9, trigger_event9, trigger_event9, trigger_event9, 
            trigger_event9, trigger_event18, trigger_event28
        ]
        selected_event = random.choice(tundra_events)
    elif setting["Jungle"] == True:
        jungle_events = [
            trigger_event2, trigger_event2, trigger_event2, trigger_event2, 
            trigger_event2, trigger_event8, trigger_event8, trigger_event8, 
            trigger_event19, trigger_event29
        ]
        selected_event = random.choice(jungle_events)
    elif setting["Plains"] == True:
        plains_events = [
            trigger_event3, trigger_event3, trigger_event3, trigger_event8, 
            trigger_event8, trigger_event8, trigger_event8, trigger_event10, 
            trigger_event10, trigger_event16, trigger_event26
        ]
        selected_event = random.choice(plains_events)
    elif setting["Desert"] == True:
        desert_events = [
            trigger_event3, trigger_event3, trigger_event3, trigger_event8, 
            trigger_event8, trigger_event8, trigger_event8, trigger_event10, 
            trigger_event10, trigger_event20, trigger_event30
        ]
        selected_event = random.choice(desert_events)
    elif setting["Mountains"] == True:
        mountains_events = [
            trigger_event12, trigger_event12, trigger_event12, trigger_event8, 
            trigger_event8, trigger_event8, trigger_event8, trigger_event2, 
            trigger_event2, trigger_event31
        ]
        selected_event = random.choice(mountains_events)
    elif setting["Ocean"] == True:
        if is_On_Water == False:
            selected_event = trigger_event8
        else:
            ocean_events = [
                trigger_event11, trigger_event11, trigger_event11, trigger_event11, 
                trigger_event11, trigger_event11, trigger_event11, trigger_event11, 
                trigger_event11, trigger_event17, trigger_pirate_attack, trigger_event27
            ]
            selected_event = random.choice(ocean_events)
    else:
        # Default to forest events if biome not recognized
        forest_events = [
            trigger_event2, trigger_event7, trigger_event8, trigger_event14, 
            trigger_event22, trigger_event24
        ]
        selected_event = random.choice(forest_events)
    
    current_event_name = selected_event.__name__
    current_text, choices = selected_event()
    buttons = [Button(50 + i*120, 400, 100, 50, c, PRIMARY_GREEN if i < len(choices)-2 else PRIMARY_BLUE) for i, c in enumerate(choices)]
    current_event = handle_event_choice

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

# Shop prices
purchase_price = {
    "Wood": 2,
    "Iron": 3,
    "Gold": 5
}

# Sell price always lower than purchase price
sell_price = {
    "Wood": 1,
    "Iron": 2,
    "Gold": 3
}

# All Weapons
weapons = {
    # Legendary Weapons (20)
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
    "Heaven's Wrath": {"rarity": "Legendary", "damage": random.randint(100, 125), "hit_chance": 85, "type": "Melee", "drop_rate": 1, "special_power": "holy"},
    "Chrono Blade": {"rarity": "Legendary", "damage": random.randint(95, 110), "hit_chance": 82, "type": "Melee", "drop_rate": 2, "special_power": "time_warp"},

    # Insane Weapons (20)
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
    "Madman's Blade": {"rarity": "Insane", "damage": random.randint(55, 75), "hit_chance": 65, "type": "Melee", "drop_rate": 35, "special_power": "berserk"},
    "Rage Spear": {"rarity": "Insane", "damage": random.randint(70, 90), "hit_chance": 60, "type": "Melee", "drop_rate": 30, "special_power": "frenzy"},
    "Night Terror": {"rarity": "Insane", "damage": random.randint(65, 85), "hit_chance": 55, "type": "Magic", "drop_rate": 40, "special_power": "fear"},
    "Acid Flail": {"rarity": "Insane", "damage": random.randint(60, 75), "hit_chance": 65, "type": "Melee", "drop_rate": 35, "special_power": "acid"},
    "Toxic Scythe": {"rarity": "Insane", "damage": random.randint(75, 95), "hit_chance": 55, "type": "Melee", "drop_rate": 30, "special_power": "toxin"},
    "Bloodfang Axe": {"rarity": "Insane", "damage": random.randint(70, 85), "hit_chance": 60, "type": "Melee", "drop_rate": 35, "special_power": "bleed"},
    "Corrupted Bow": {"rarity": "Insane", "damage": random.randint(50, 70), "hit_chance": 70, "type": "Ranged", "drop_rate": 40, "special_power": "curse"},
    "Soulfire Staff": {"rarity": "Insane", "damage": random.randint(45, 60), "hit_chance": 75, "type": "Magic", "drop_rate": 35, "special_power": "curse"},
    "Ruin Blade": {"rarity": "Insane", "damage": random.randint(85, 105), "hit_chance": 50, "type": "Melee", "drop_rate": 25, "special_power": "destruction"},
    "Howling Pike": {"rarity": "Insane", "damage": random.randint(60, 85), "hit_chance": 65, "type": "Melee", "drop_rate": 40, "special_power": "scream"},

    # Rare Weapons (20)
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

    # Uncommon Weapons (20)
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
    "Hunter's Bow": {"rarity": "Uncommon", "damage": random.randint(12, 19), "hit_chance": 72, "type": "Ranged", "drop_rate": 75, "special_power": "none"},
    "Forged Spear": {"rarity": "Uncommon", "damage": random.randint(18, 25), "hit_chance": 68, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Steel Dagger": {"rarity": "Uncommon", "damage": random.randint(15, 20), "hit_chance": 80, "type": "Melee", "drop_rate": 80, "special_power": "none"},
    "Iron Pike": {"rarity": "Uncommon", "damage": random.randint(17, 23), "hit_chance": 65, "type": "Melee", "drop_rate": 75, "special_power": "none"},
    "Runed Mace": {"rarity": "Uncommon", "damage": random.randint(16, 21), "hit_chance": 70, "type": "Melee", "drop_rate": 70, "special_power": "none"},
    "Reinforced Staff": {"rarity": "Uncommon", "damage": random.randint(10, 16), "hit_chance": 75, "type": "Magic", "drop_rate": 80, "special_power": "none"},
    "Wooden Bow": {"rarity": "Uncommon", "damage": random.randint(10, 15), "hit_chance": 70, "type": "Ranged", "drop_rate": 80, "special_power": "none"},
    "Chipped Axe": {"rarity": "Uncommon", "damage": random.randint(12, 18), "hit_chance": 65, "type": "Melee", "drop_rate": 85, "special_power": "none"},
    "Bronze Mace": {"rarity": "Uncommon", "damage": random.randint(13, 19), "hit_chance": 68, "type": "Melee", "drop_rate": 75, "special_power": "none"},

    # Common Weapons (20)
    "Iron Sword": {"rarity": "Common", "damage": random.randint(10, 20), "hit_chance": 60, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Sturdy Sword": {"rarity": "Common", "damage": random.randint(7, 15), "hit_chance": 70, "type": "Melee", "drop_rate": 95, "special_power": "none"},
    "Rusty Sword": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 70, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Wooden Staff": {"rarity": "Common", "damage": random.randint(5, 10), "hit_chance": 70, "type": "Magic", "drop_rate": 100, "special_power": "none"},
    "Training Dagger": {"rarity": "Common", "damage": random.randint(3, 7), "hit_chance": 85, "type": "Melee", "drop_rate": 100, "special_power": "none"},
    "Farmer's Pitchfork": {"rarity": "Common", "damage": random.randint(5, 12), "hit_chance": 60, "type": "Melee", "drop_rate": 100, "special_power": "none"},
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

    # Empty Weapon (1)
    "Fist": {"rarity": "None", "damage": 3, "hit_chance": 70, "type": "Melee", "drop_rate": 0, "special_power": "none"}
}

spells = {
    # Air / Wind
    "Wind Spell": {"damage": random.randint(5, 8), "hit_chance": 95, "mana_cost": 1, "special_power": "none"},
    "Gust": {"damage": random.randint(8, 15), "hit_chance": 70, "mana_cost": 2, "special_power": "none"},
    "Hurricane": {"damage": random.randint(25, 35), "hit_chance": 50, "mana_cost": 8, "special_power": "stun"},
    "Whirlwind": {"damage": random.randint(18, 28), "hit_chance": 65, "mana_cost": 5, "special_power": "none"},
    "Zephyr Slash": {"damage": random.randint(12, 20), "hit_chance": 75, "mana_cost": 3, "special_power": "none"},

    # Ice
    "Ice Blast": {"damage": random.randint(10, 20), "hit_chance": 60, "mana_cost": 3, "special_power": "ice"},
    "Frost Spike": {"damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "ice"},
    "Glacier": {"damage": random.randint(30, 40), "hit_chance": 50, "mana_cost": 9, "special_power": "ice"},
    "Snowstorm": {"damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "blind"},
    "Frozen Shards": {"damage": random.randint(18, 24), "hit_chance": 70, "mana_cost": 5, "special_power": "bleed"},

    # Lightning
    "Lightning Bolt": {"damage": random.randint(15, 20), "hit_chance": 75, "mana_cost": 3, "special_power": "stun"},
    "Thunder Strike": {"damage": random.randint(20, 30), "hit_chance": 65, "mana_cost": 5, "special_power": "stun"},
    "Charge Blast": {"damage": random.randint(15, 25), "hit_chance": 70, "mana_cost": 6, "special_power": "stun"},
    "Storm Surge": {"damage": random.randint(25, 35), "hit_chance": 55, "mana_cost": 7, "special_power": "stun"},
    "Ball Lightning": {"damage": random.randint(18, 26), "hit_chance": 65, "mana_cost": 5, "special_power": "fire"},

    # Fire
    "Fireball": {"damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "fire"},
    "Flame Wave": {"damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 5, "special_power": "fire"},
    "Inferno": {"damage": random.randint(35, 50), "hit_chance": 50, "mana_cost": 10, "special_power": "fire"},
    "Ember Shot": {"damage": random.randint(8, 15), "hit_chance": 80, "mana_cost": 2, "special_power": "fire"},
    "Dragon's Breath": {"damage": random.randint(25, 40), "hit_chance": 55, "mana_cost": 7, "special_power": "fire"},

    # Water
    "Water Jet": {"damage": random.randint(12, 20), "hit_chance": 70, "mana_cost": 3, "special_power": "none"},
    "Tidal Wave": {"damage": random.randint(28, 38), "hit_chance": 55, "mana_cost": 8, "special_power": "stun"},
    "Bubble Prison": {"damage": random.randint(8, 12), "hit_chance": 85, "mana_cost": 4, "special_power": "none"},
    "Aqua Slash": {"damage": random.randint(15, 22), "hit_chance": 75, "mana_cost": 3, "special_power": "bleed"},
    "Rainstorm": {"damage": random.randint(18, 25), "hit_chance": 70, "mana_cost": 5, "special_power": "none"},

    # Earth
    "Rock Throw": {"damage": random.randint(10, 18), "hit_chance": 70, "mana_cost": 3, "special_power": "none"},
    "Earthquake": {"damage": random.randint(30, 45), "hit_chance": 50, "mana_cost": 9, "special_power": "stun"},
    "Stone Spike": {"damage": random.randint(15, 25), "hit_chance": 65, "mana_cost": 4, "special_power": "none"},
    "Sandstorm": {"damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "blind"},
    "Iron Fist": {"damage": random.randint(18, 26), "hit_chance": 70, "mana_cost": 5, "special_power": "broken_armor"},

    # Dark
    "Shadow Bolt": {"damage": random.randint(15, 25), "hit_chance": 70, "mana_cost": 4, "special_power": "curse"},
    "Nightmare": {"damage": random.randint(25, 35), "hit_chance": 55, "mana_cost": 7, "special_power": "curse"},
    "Soul Drain": {"damage": random.randint(12, 20), "hit_chance": 65, "mana_cost": 5, "special_power": "vampiric"},
    "Dark Wave": {"damage": random.randint(20, 30), "hit_chance": 60, "mana_cost": 6, "special_power": "curse"},
    "Abyssal Flame": {"damage": random.randint(30, 40), "hit_chance": 50, "mana_cost": 8, "special_power": "burn"},

    # Holy / Light
    "Holy Beam": {"damage": random.randint(15, 25), "hit_chance": 75, "mana_cost": 4, "special_power": "heal"},
    "Radiant Slash": {"damage": random.randint(20, 30), "hit_chance": 70, "mana_cost": 5, "special_power": "blind"},
    "Healing Light": {"damage": 0, "hit_chance": 100, "mana_cost": 6, "special_power": "heal"},
    "Smite": {"damage": random.randint(25, 35), "hit_chance": 65, "mana_cost": 7, "special_power": "burn"},
    "Sunburst": {"damage": random.randint(30, 40), "hit_chance": 55, "mana_cost": 9, "special_power": "burn"},

    # Arcane / Utility
    "Arcane Missile": {"damage": random.randint(12, 20), "hit_chance": 80, "mana_cost": 3, "special_power": "none"},
    "Mana Burn": {"damage": random.randint(10, 15), "hit_chance": 70, "mana_cost": 4, "special_power": "mana_drain"},
    "Time Stop": {"damage": 0, "hit_chance": 100, "mana_cost": 12, "special_power": "stun"},
    "Teleport Strike": {"damage": random.randint(20, 28), "hit_chance": 85, "mana_cost": 6, "special_power": "teleport"},
    "Mirror Image": {"damage": 0, "hit_chance": 100, "mana_cost": 5, "special_power": "confusion"},
}

current_spells = {}

# Pre-enabled Stats
max_HP = 20
max_Mana = 20
critical_chance = 15

# Event Flags
is_Victorious = False
is_On_Water = False
is_Thirsty = False

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

# Shop prices
purchase_price = {
    "Wood": 2,
    "Iron": 3,
    "Gold": 5
}

# Sell price always lower than purchase price
sell_price = {
    "Wood": 1,
    "Iron": 2,
    "Gold": 3
}

list_of_classes = ["1. Warrior", "2. Mage", "3. Defender"]
# Player starts with 3 slots
player_weapons = ["Fist", "Fist", "Fist"]

# Game Start - Now handled by Pygame GUI
# print("To play, type in the number of the option you would like to choose.\nWelcome to Löwengarde! A magical place of destiny, heroes, and courage. We welcome you with all our hearts, and wish you a wonderful stay! Unfortunately, now isn't the best time to come for a vacation or a lolly, as there has been a major insurrection among the government of the united race tribes, and an evil ogre named NAME has taken over, enforcing all under his rule to work as his servants and slave away for no money, and what little we do receive is taxed.\nSay, you appear to be a noble warrior, and therefore we would petition your help. What kind of warrior are you, new friend?\n1. Warrior\n2. Mage\n3. Defender")

chosen_class = None

# Main game loop
def main():
    global current_text, game_started, buttons, chosen_class

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Löwengarde Adventure")

    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(60)  # 60 FPS
        bg_color = biome_colors.get(current_biome, PRIMARY_BLUE)
        screen.fill(bg_color)

        # === TOP BAR WITH STATS ===
        top_bar_height = 60
        pygame.draw.rect(screen, (255, 255, 255, 200), (0, 0, SCREEN_WIDTH, top_bar_height))
        pygame.draw.line(screen, PRIMARY_GREEN, (0, top_bar_height), (SCREEN_WIDTH, top_bar_height), 3)
        
        # Display top stats as badges
        stat_items = [
            (f"❤️ {character_statistics['HP']}/{max_HP}", DANGER_RED),
            (f"💙 {character_statistics['Mana']}/{max_Mana}", PRIMARY_BLUE),
            (f"⚡ LV {character_statistics.get('Level', 1)}", PRIMARY_GREEN),
        ]
        
        x_offset = 20
        for stat_text, stat_color in stat_items:
            badge_surf = font.render(stat_text, True, WHITE)
            badge_rect = badge_surf.get_rect(topleft=(x_offset, 18))
            
            # Badge background
            bg_rect = badge_rect.inflate(16, 12)
            pygame.draw.rect(screen, stat_color, bg_rect, border_radius=6)
            screen.blit(badge_surf, badge_rect)
            x_offset += badge_rect.width + 40

        # === EVENT TEXT BOX ===
        event_x, event_y = 40, 80
        event_width, event_height = SCREEN_WIDTH - 80, 280
        
        # Shadow effect
        shadow_rect = pygame.Rect(event_x + 2, event_y + 2, event_width, event_height)
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=12)
        
        # Main box
        pygame.draw.rect(screen, WHITE, (event_x, event_y, event_width, event_height), border_radius=12)
        pygame.draw.rect(screen, PRIMARY_GREEN, (event_x, event_y, event_width, event_height), 3, border_radius=12)
        
        # Event text with wrapping
        wrapped_lines = []
        for paragraph in current_text.split('\n'):
            wrapped_lines.extend(wrap_text(paragraph, font, event_width - 40))
        
        text_y = event_y + 20
        for line in wrapped_lines:
            text_surf = font.render(line, True, BLACK)
            screen.blit(text_surf, (event_x + 20, text_y))
            text_y += 28
            if text_y > event_y + event_height - 20:
                break

        # === BUTTONS SECTION ===
        button_y = event_y + event_height + 30
        button_width = 140
        button_height = 50
        button_spacing = 20
        
        # Center buttons
        total_buttons = len(buttons)
        total_width = total_buttons * button_width + (total_buttons - 1) * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, button in enumerate(buttons):
            button.rect.x = start_x + i * (button_width + button_spacing)
            button.rect.y = button_y
            button.rect.width = button_width
            button.rect.height = button_height
            button.draw(screen)

        # === STATS PANEL ===
        stats_y = button_y + button_height + 20
        stats_height = SCREEN_HEIGHT - stats_y - 10
        
        pygame.draw.rect(screen, WHITE, (40, stats_y, SCREEN_WIDTH - 80, stats_height), border_radius=10)
        pygame.draw.rect(screen, PRIMARY_BLUE, (40, stats_y, SCREEN_WIDTH - 80, stats_height), 2, border_radius=10)
        
        # Stats title
        title_surf = font.render("⚔️ Character Stats", True, PRIMARY_BLUE)
        screen.blit(title_surf, (60, stats_y + 10))
        
        # Stats in two columns with color badges
        stat_configs = [
            ("STR", character_statistics.get("Strength", 0), STRENGTH_COLOR),
            ("DEF", character_statistics.get("Defense", 0), DEFENSE_COLOR),
            ("MAG", character_statistics.get("Magic", 0), MAGIC_COLOR),
            ("DEX", character_statistics.get("Dexterity", 0), DEXTERITY_COLOR),
            ("SPD", character_statistics.get("Speed", 0), SPEED_COLOR),
            ("INT", character_statistics.get("Intellect", 0), INTELLECT_COLOR),
        ]
        
        stat_x_offset = 60
        stat_y_offset = stats_y + 40
        col_count = 0
        
        for label, value, color in stat_configs:
            # Stat badge
            badge_width = 120
            badge_rect = pygame.Rect(stat_x_offset + (col_count % 3) * (badge_width + 30),
                                     stat_y_offset + (col_count // 3) * 35,
                                     badge_width, 30)
            
            pygame.draw.rect(screen, color, badge_rect, border_radius=6)
            stat_text = f"{label}: {value}"
            stat_surf = font.render(stat_text, True, WHITE)
            stat_rect = stat_surf.get_rect(center=badge_rect.center)
            screen.blit(stat_surf, stat_rect)
            
            col_count += 1

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                if button.is_clicked(event):
                    if current_event is not None:
                        current_event(button.text)
                    else:
                        handle_choice(button.text)

    pygame.quit()

def handle_choice(choice):
    global current_text, game_started, buttons, chosen_class

    if not game_started:
        if choice == "Warrior":
            chosen_class = 1
            character_statistics["Strength"] += 10
            player_weapons[0] = "Sturdy Sword"
            current_text = "Ah, a warrior! Strong with the sword, mighty with the bow! Truly the fighter we always desired! We believe in you warrior, we know you can set us free from the tyrannical king NAME\nYou begin the game with 10 Strength and a Sturdy Sword"
            game_started = True
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        elif choice == "Mage":
            chosen_class = 2
            max_Mana = 30
            character_statistics["Mana"] = 30
            character_statistics["Magic"] += 10
            current_spells["Wind Spell"] = 1
            player_weapons[0] = "Wooden Staff"
            current_text = "Ah, a mage! A mind like a tempest, and a desire burning like fire! Truly the fighter we always desired! We believe in you mage, we know you can set us free from the tyrannical king NAME\nYou begin the game with 10 Magic, a Sturdy Sword, and a simple Wind Spell"
            game_started = True
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
        elif choice == "Defender":
            chosen_class = 3
            character_statistics["Defense"] += 10
            player_weapons[0] = "Rusty Sword"
            current_text = "Ah, a defender! Hard like a rock, impenetrable, and ready to protect at all costs! Truly the fighter we always desired! We believe in you defender, we know you can set us free from the tyrannical king NAME\nYou begin the game with 10 Defense and a Rusty Sword"
            game_started = True
            buttons = [Button(50, 400, 120, 50, "Continue", PRIMARY_GREEN)]
    else:
        if choice == "Continue":
            if current_event is None:
                # Continue to next event after completing previous one
                trigger_random_event()
            else:
                # Start the game loop
                current_text = "Starting your adventure..."
                buttons = [Button(50, 400, 120, 50, "Next Event", PRIMARY_GREEN)]
        elif choice == "Next Event":
            # Call the main game loop logic here
            trigger_random_event()
        elif choice == "Stats":
            # Open profile.html in browser
            profile_path = os.path.join(os.path.dirname(__file__), "profile.html")
            webbrowser.open(f"file://{profile_path}")
        elif choice == "Inventory":
            # Open inventory.html in browser
            inventory_path = os.path.join(os.path.dirname(__file__), "inventory.html")
            webbrowser.open(f"file://{inventory_path}")

if __name__ == "__main__":
    main()
