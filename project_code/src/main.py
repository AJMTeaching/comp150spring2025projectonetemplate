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
    def __init__(self, name: str, health: int = 10, max_health: int = 10, coins: int = 0):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.inventory = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities = []
        self.coins = coins
    
    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")
    
    def regenerate_health(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        print(f"{self.name} regenerates {amount} health! Current Health: {self.health}")
    
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
        super().__init__(name="Wizard Cat", health=12, max_health=12, coins=5)
        self.add_ability("Fireball")
        self.add_ability("Magic Shield")

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15, max_health=15, coins=3)
        self.add_ability("Forsaken Furball")
        self.add_ability("Cowardice")

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10, max_health=10, coins=7)
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
        print("1. Attack")
        print("2. Regenerate Health")
        choice = UserInputHandler.get_valid_number("Enter action number: ", 1, 2)
        
        if choice == 1:
            damage = random.randint(3, 7)
            print(f"{player.name} attacks and deals {damage} damage!")
            enemy.take_damage(damage)
        elif choice == 2:
            regen_amount = random.randint(3, 6)
            player.regenerate_health(regen_amount)
        
        if enemy.health <= 0:
            print(f"{enemy.name} is defeated!")
            return True
        
        print(f"{enemy.name} attacks!")
        player.take_damage(enemy.damage)
        if player.health <= 0:
            print(f"{player.name} has been defeated...")
            return False

# --- START GAME ---
if __name__ == "__main__":
    play_game()
