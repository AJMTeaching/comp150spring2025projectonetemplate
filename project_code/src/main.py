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

# --- CHARACTER CLASSES ---
class Character:
    def __init__(self, name: str, health: int = 10, coins: int = 0):
        self.name = name
        self.health = health
        self.inventory = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities = []
        self.coins = coins
    
    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")
    
    def add_ability(self, ability):
        self.abilities.append(ability)

    def earn_coins(self, amount: int):
        self.coins += amount
        print(f"{self.name} earned {amount} coins! Total: {self.coins}")

    def spend_coins(self, amount: int):
        if self.coins >= amount:
            self.coins -= amount
            print(f"{self.name} spent {amount} coins. Remaining: {self.coins}")
        else:
            print("Not enough coins!")

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12, coins=5)
        self.add_ability("Fireball")
        self.add_ability("Magic Shield")

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15, coins=3)
        self.add_ability("Forsaken Furball")
        self.add_ability("Cowardice")

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10, coins=7)
        self.add_ability("Nuclear Reactivity")

# --- SHOP SYSTEM ---
class Shop:
    def __init__(self):
        self.items = {"Health Potion": 3, "Strength Boost": 5, "Intelligence Boost": 5}

    def display_items(self):
        print("Welcome to the Shop! Available items:")
        for item, price in self.items.items():
            print(f"{item}: {price} coins")

    def purchase(self, player: Character):
        self.display_items()
        choice = UserInputHandler.get_valid_input("What would you like to buy? (Enter item name or 'exit' to leave): ", list(self.items.keys()) + ["exit"])
        if choice != "exit":
            price = self.items[choice]
            if player.coins >= price:
                player.spend_coins(price)
                player.inventory.append(choice)
                print(f"{player.name} purchased {choice}!")
            else:
                print("Not enough coins!")

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
    shop = Shop()
    
    for mission in range(1, 4):
        print(f"Mission {mission}: Travel to {random.choice(locations)}")
        enemy = Enemy("Claw Bandit", 7, random.randint(2, 5))
        
        if combat(player, enemy):
            artifacts_collected += 1
            player.earn_coins(5)
            print("You found an artifact! Abilities unlocked.")
            if artifacts_collected == 3:
                print("All abilities unlocked! You are ready for the final battle.")
        else:
            print("Game Over! Try again.")
            return
        
        shop.purchase(player)
    
    print("\nFinal Battle: The Barking Kitten War General appears!")
    final_boss = Enemy("Barking Kitten War General", 14, 5)
    if combat(player, final_boss):
        print("Congratulations! You have defeated the War General and saved the Kitten Kingdom!")
    else:
        print("You were defeated... The Kitten Kingdom falls into chaos!")

# --- START GAME ---
if __name__ == "__main__":
    play_game()
