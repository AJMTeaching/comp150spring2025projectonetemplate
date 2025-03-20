import json
import random
from typing import List
from enum import Enum

# --- ENUMS ---
class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"

# --- STATISTIC CLASS ---
class Statistic:
    def __init__(self, name: str, value: int = 0, min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))

# --- CHARACTER CLASSES ---
class Character:
    def __init__(self, name: str, health: int = 10):
        self.name = name
        self.health = health
        self.inventory = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities = []
    
    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")
    
    def add_ability(self, ability):
        self.abilities.append(ability)

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12)
        self.add_ability("Fireball")
        self.add_ability("Magic Shield")

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15)
        self.add_ability("Forsaken Furball")
        self.add_ability("Cowardice")

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10)
        self.add_ability("Nuclear Reactivity")

# --- ENEMY CLASS ---
class Enemy:
    def __init__(self, name: str, health: int, damage: int):
        self.name = name
        self.health = health
        self.damage = damage
    
    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")

# --- INPUT HANDLING CLASS ---
class UserInputHandler:
    @staticmethod
    def get_valid_input(prompt: str, options: List[str]):
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in options:
                return user_input
            print("Invalid input! Please choose a valid option.")
    
    @staticmethod
    def get_valid_number(prompt: str, min_val: int, max_val: int):
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")

# --- COMBAT SYSTEM ---
def combat(player: Character, enemy: Enemy):
    print(f"{player.name} engages in battle with {enemy.name}!")
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name}'s turn! Choose an ability:")
        for idx, ability in enumerate(player.abilities):
            print(f"{idx + 1}. {ability}")
        choice = UserInputHandler.get_valid_number("Enter ability number: ", 1, len(player.abilities)) - 1
        damage = random.randint(3, 7)  # Randomized damage output
        print(f"{player.name} used {player.abilities[choice]} and dealt {damage} damage!")
        enemy.take_damage(damage)
        
        if enemy.health <= 0:
            print(f"{enemy.name} is defeated!")
            return True
        
        print(f"{enemy.name} attacks!")
        player.take_damage(enemy.damage)
        if player.health <= 0:
            print(f"{player.name} has been defeated...")
            return False

# --- GAME LOGIC ---
def choose_character():
    print("Choose your kitten:")
    choices = {"1": WizardCat, "2": FeralCat, "3": ExplodingKitten}
    user_choice = UserInputHandler.get_valid_input("1. Wizard Cat\n2. Feral Cat\n3. Exploding Kitten\nEnter your choice: ", choices.keys())
    return choices[user_choice]()

def play_game():
    print("Welcome to Exploding Kittens: The RPG!")
    player = choose_character()
    print(f"You have chosen: {player.name}\n")
    
    locations = [
        "The Clawed Goblet", "Felis Infernum", "The Witherwild Thicket",
        "Purrgatory Dungeon", "Meowntain Fortress", "The Neon Alley", "Shadowclaw Ruins", "The Golden Litterbox"
    ]
    artifacts_collected = 0
    
    for mission in range(1, 4):
        print(f"Mission {mission}: Travel to {random.choice(locations)}")
        enemy = Enemy("Claw Bandit", 7, random.randint(2, 5))
        
        if combat(player, enemy):
            artifacts_collected += 1
            print("You found an artifact! Abilities unlocked.")
            if artifacts_collected == 3:
                print("All abilities unlocked! You are ready for the final battle.")
        else:
            print("Game Over! Try again.")
            return
    
    print("\nFinal Battle: The Barking Kitten War General appears!")
    final_boss = Enemy("Barking Kitten War General", 14, 5)
    if combat(player, final_boss):
        print("Congratulations! You have defeated the War General and saved the Kitten Kingdom!")
    else:
        print("You were defeated... The Kitten Kingdom falls into chaos!")

# --- START GAME ---
if __name__ == "__main__":
    play_game()
