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
        self.max_health = health
        self.inventory = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities = []
        self.coins = coins

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")

    def heal(self):
        if random.random() < (2 / 3):
            heal_amount = random.randint(5, 10)
            self.health = min(self.max_health, self.health + heal_amount)
            print(f"{self.name} healed for {heal_amount} health! Current Health: {self.health}")
        else:
            print(f"{self.name} tried to heal, but it failed!")

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

# --- ENEMY CLASS ---
class Enemy:
    def __init__(self, name: str, health: int, damage: int):
        self.name = name
        self.health = health
        self.damage = damage

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")

# --- COMBAT SYSTEM ---
def combat(player: Character, enemy: Enemy):
    print(f"{player.name} engages in battle with {enemy.name}!")
    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name}'s turn! Choose an action:")
        print("1. Use Ability")
        print("2. Attempt to Heal")
        action = UserInputHandler.get_valid_number("Enter action number: ", 1, 2)

        if action == 1:
            print("Choose an ability:")
            for idx, ability in enumerate(player.abilities):
                print(f"{idx + 1}. {ability}")
            choice = UserInputHandler.get_valid_number("Enter ability number: ", 1, len(player.abilities)) - 1
            damage = random.randint(3, 7)
            print(f"{player.name} used {player.abilities[choice]} and dealt {damage} damage!")
            enemy.take_damage(damage)
        elif action == 2:
            player.heal()

        if enemy.health <= 0:
            print(f"{enemy.name} is defeated!")
            return True

        print(f"{enemy.name} attacks!")
        player.take_damage(enemy.damage)
        if player.health <= 0:
            print(f"{player.name} has been defeated...")
            return False

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

def choose_location(locations: List[str]) -> str:
    print("Choose a location to explore:")
    for idx, loc in enumerate(locations, 1):
        print(f"{idx}. {loc}")
    choice = UserInputHandler.get_valid_number("Enter location number: ", 1, len(locations)) - 1
    return locations[choice]

def play_game():
    print("Welcome to Exploding Kittens: The RPG!")
    print("The Kitten Military Forces have defended their territory with precision and finesse.")
    print("However, there has been a security breach detected at the main base!")
    print("You are a new recruit, ready to serve. The whole base is on lockdown and Sergeant Barking Kitten takes you under his paw!")
    print("With a tiny meow, he demands you to: >\"There's an intruder in our ranks, rookie! If you want to survive, you need to learn some skills fast!\"")
    print("Your mission is clear: Find the Intruder and eliminate the threat!\n")

    player = choose_character()
    print(f"You have chosen: {player.name}\n")

    locations = ["The Clawed Goblet", "Felis Infernum", "The Witherwild Thicket", "The Purrgola", "Felis Elysium"]
    for _ in range(3):
        location = choose_location(locations)
        print(f"Exploring {location}...")
        if location == "The Clawed Goblet":
            enemy = Enemy("Claw Bandit", 7, random.randint(2, 5))
        elif location == "Felis Infernum":
            enemy = Enemy("Flame Paw", 8, random.randint(3, 6))
        elif location == "The Witherwild Thicket":
            enemy = Enemy("Ghost Whisker", 6, random.randint(2, 5))
        elif location == "The Purrgola":
            enemy = Enemy("Sunning Saboteur", 7, random.randint(2, 4))
        elif location == "Felis Elysium":
            enemy = Enemy("Halo Pouncer", 9, random.randint(3, 6))

        victory = combat(player, enemy)
        elif location == "Felis Infernum":
        enemy = Enemy("Flame Paw", 8, random.randint(3, 6))
        elif location == "The Witherwild Thicket":
        enemy = Enemy("Ghost Whisker", 6, random.randint(2, 5))
        elif location == "The Purrgola":
        enemy = Enemy("Sunning Saboteur", 7, random.randint(2, 4))
        elif location == "Felis Elysium":
        enemy = Enemy("Halo Pouncer", 9, random.randint(3, 6))
        if victory:
            player.max_health += 1
            player.health = player.max_health
            print(f"{player.name} has grown stronger! Max health is now {player.max_health}.")
        if victory:
            player.max_health += 1
            player.health = player.max_health
            print(f"{player.name} has grown stronger! Max health is now {player.max_health}.")

    print("Final Battle: The Barking Kitten War General appears!")
    final_boss = Enemy("Barking Kitten War General", 14, 5)
    if combat(player, final_boss):
        print("Congratulations! You defeated the Barking Kitten War General.")
    else:
        print("Game Over! You were defeated by the Barking Kitten War General. Rest in Peace, soldier.")

# --- START GAME ---
if __name__ == "__main__":
    play_game()
