import json
import random
from typing import List, Dict, Optional
from enum import Enum
from abc import ABC, abstractmethod
import sys

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

    def modify(self, amount: int) -> int:
        self.value = max(self.min_value, min(self.max_value, self.value + amount))
        return self.value

# --- GAME ENTITY BASE CLASS ---
class GameEntity(ABC):
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
        self.max_health = health

    def take_damage(self, amount: int) -> int:
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")
        return self.health

    def is_alive(self) -> bool:
        return self.health > 0

# --- ABILITY CLASS ---
class Ability:
    def __init__(self, name: str, damage_range: tuple = (3, 7), chance_to_hit: float = 0.9):
        self.name = name
        self.damage_range = damage_range
        self.chance_to_hit = chance_to_hit

    def use(self, user: 'Character', target: GameEntity) -> bool:
        if random.random() <= self.chance_to_hit:
            damage = random.randint(*self.damage_range)
            if hasattr(user, 'strength'):
                damage += user.strength.value // 3
            print(f"{user.name} used {self.name} and dealt {damage} damage!")
            target.take_damage(damage)
            return True
        else:
            print(f"{user.name} used {self.name} but missed!")
            return False

# --- INPUT HANDLING CLASS ---
class UserInputHandler:
    @staticmethod
    def get_valid_input(prompt: str, options: List[str]) -> str:
        options_lower = [opt.lower() for opt in options]
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in options_lower:
                return options[options_lower.index(user_input)]
            print(f"Invalid input! Please choose from: {', '.join(options)}")

    @staticmethod
    def get_valid_number(prompt: str, min_val: int, max_val: int) -> int:
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")

# --- ITEM CLASS ---
class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def use(self, character: 'Character') -> bool:
        print(f"{character.name} used {self.name}!")
        return True

class HealthPotion(Item):
    def __init__(self, healing_range: tuple = (5, 10)):
        super().__init__(name="Health Potion", description="Restores health")
        self.healing_range = healing_range

    def use(self, character: 'Character') -> bool:
        if character.health < character.max_health:
            heal_amount = random.randint(*self.healing_range)
            old_health = character.health
            character.health = min(character.max_health, character.health + heal_amount)
            actual_healing = character.health - old_health
            print(f"{character.name} healed for {actual_healing} health! Current Health: {character.health}")
            return True
        else:
            print(f"{character.name} is already at full health!")
            return False

# --- CHARACTER CLASSES ---
class Character(GameEntity):
    def __init__(self, name: str, health: int = 10):
        super().__init__(name, health)
        self.inventory: List[Item] = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities: List[Ability] = []

    def heal(self) -> bool:
        if random.random() < (2 / 3):
            heal_amount = random.randint(5, 10)
            old_health = self.health
            self.health = min(self.max_health, self.health + heal_amount)
            actual_healing = self.health - old_health
            print(f"{self.name} healed for {actual_healing} health! Current Health: {self.health}")
            return True
        else:
            print(f"{self.name} tried to heal, but it failed!")
            return False

    def add_ability(self, ability: Ability) -> None:
        self.abilities.append(ability)

    def use_item_from_inventory(self, item_index: int) -> bool:
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.use(self):
                self.inventory.pop(item_index)
                return True
        return False

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12)
        self.intelligence.value = 8
        self.add_ability(Ability("Fireball", damage_range=(4, 8)))
        self.add_ability(Ability("Magic Shield", damage_range=(2, 5)))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15)
        self.strength.value = 8
        self.add_ability(Ability("Forsaken Furball", damage_range=(5, 9)))
        self.add_ability(Ability("Cowardice", damage_range=(3, 6)))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10)
        self.add_ability(Ability("Nuclear Reactivity", damage_range=(4, 10)))
        self.add_ability(Ability("Controlled Explosion", damage_range=(3, 7)))

# --- ENEMY CLASS ---
class Enemy(GameEntity):
    def __init__(self, name: str, health: int, damage_range: tuple = (2, 5)):
        super().__init__(name, health)
        self.damage_range = damage_range

    def attack(self, target: Character) -> int:
        damage = random.randint(*self.damage_range)
        print(f"{self.name} attacks for {damage} damage!")
        target.take_damage(damage)
        return damage

# --- COMBAT SYSTEM ---
def combat(player: Character, enemy: Enemy) -> bool:
    print(f"{player.name} engages in battle with {enemy.name}!")
    print(f"{enemy.name}: 'You shall not claw past me so easily!'")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name}'s turn! Health: {player.health}/{player.max_health}")
        print("Choose an action:")
        print("1. Use Ability")
        print("2. Attempt to Heal")
        if player.inventory:
            print("3. Use Item")
            max_choice = 3
        else:
            max_choice = 2

        action = UserInputHandler.get_valid_number("Enter action number: ", 1, max_choice)

        if action == 1:
            print("Choose an ability:")
            for idx, ability in enumerate(player.abilities):
                print(f"{idx + 1}. {ability.name}")
            choice = UserInputHandler.get_valid_number("Enter ability number: ", 1, len(player.abilities)) - 1
            player.abilities[choice].use(player, enemy)
        elif action == 2:
            player.heal()
        elif action == 3 and player.inventory:
            print("Choose an item:")
            for idx, item in enumerate(player.inventory):
                print(f"{idx + 1}. {item.name} - {item.description}")
            choice = UserInputHandler.get_valid_number("Enter item number: ", 1, len(player.inventory)) - 1
            player.use_item_from_inventory(choice)

        if not enemy.is_alive():
            print(f"{enemy.name} is defeated!")
            print(f"{player.name}: 'Another one bites the fur!'")
            return True

        print(f"\n{enemy.name}'s turn! Health: {enemy.health}")
        enemy.attack(player)

        if not player.is_alive():
            print(f"{player.name} has been defeated... The intruder still roams free.")
            return False

    return player.is_alive()

# --- GAME STATE ---
class GameState:
    def __init__(self):
        self.player: Optional[Character] = None
        self.locations_visited = 0
        self.max_locations = 3

# --- LOCATION AND ENEMY GENERATION ---
def get_location_enemy(location: str) -> Enemy:
    if location == "The Clawed Goblet":
        return Enemy("Claw Bandit", 7, damage_range=(2, 5))
    elif location == "Felis Infernum":
        return Enemy("Flame Paw", 8, damage_range=(3, 6))
    elif location == "The Witherwild Thicket":
        return Enemy("Ghost Whisker", 6, damage_range=(2, 5))
    elif location == "The Purrgola":
        return Enemy("Sunning Saboteur", 7, damage_range=(2, 4))
    elif location == "Felis Elysium":
        return Enemy("Halo Pouncer", 9, damage_range=(3, 6))
    else:
        return Enemy("Mysterious Cat", 7, damage_range=(2, 5))

# --- GAME LOGIC ---
def choose_character() -> Character:
    print("Choose your kitten:")
    choices = {
        "1": WizardCat,
        "2": FeralCat,
        "3": ExplodingKitten
    }
    descriptions = {
        "1": "Wizard Cat - Higher intelligence, magical abilities",
        "2": "Feral Cat - Higher strength, physical prowess",
        "3": "Exploding Kitten - Balanced stats, explosive abilities"
    }

    for key, desc in descriptions.items():
        print(f"{key}. {desc}")

    user_choice = UserInputHandler.get_valid_input("Enter your choice: ", list(choices.keys()))
    return choices[user_choice]()

def choose_location(locations: List[str], visited: List[str]) -> str:
    print("Choose a location to explore:")
    for idx, loc in enumerate(locations, 1):
        status = " (visited)" if loc in visited else ""
        print(f"{idx}. {loc}{status}")
    choice = UserInputHandler.get_valid_number("Enter location number: ", 1, len(locations)) - 1
    return locations[choice]

def play_game() -> None:
    print("Welcome to Exploding Kittens: The RPG!")
    print("Your mission is clear: Find the Intruder and eliminate the threat!\n")

    game_state = GameState()
    game_state.player = choose_character()
    print(f"You have chosen: {game_state.player.name}\n")
    game_state.player.inventory.append(HealthPotion())
    print(f"You received a Health Potion to start your journey!")

    locations = ["The Clawed Goblet", "Felis Infernum", "The Witherwild Thicket", "The Purrgola", "Felis Elysium"]
    visited_locations = []

    while game_state.locations_visited < game_state.max_locations and game_state.player.is_alive():
        location = choose_location(locations, visited_locations)
        visited_locations.append(location)
        game_state.locations_visited += 1

        print(f"\nExploring {location}...")
        enemy = get_location_enemy(location)
        victory = combat(game_state.player, enemy)
        if victory:
            game_state.player.max_health += 1
            game_state.player.health = game_state.player.max_health
            print(f"{game_state.player.name} has grown stronger! Max health is now {game_state.player.max_health}.")
        else:
            print("Game Over! You were defeated!")
            return

    if game_state.player.is_alive():
        print("\nFinal Battle: The Barking Kitten War General appears from the shadows!")
        print("Barking Kitten War General: 'You've made it far, but this is where your journey ends, rookie!'")
        final_boss = Enemy("Barking Kitten War General", 14, damage_range=(4, 7))
        if combat(game_state.player, final_boss):
            print("Congratulations! You defeated the Barking Kitten War General.")
            print("The Kitten Military Forces are saved, and you become a hero among cats!")
        else:
            print("Game Over! You were defeated by the Barking Kitten War General. Rest in Peace, soldier.")

# --- UNIT TESTS ---
import unittest
from unittest.mock import patch

class TestStatistic(unittest.TestCase):
    def test_modify_increase_within_bounds(self):
        stat = Statistic("Test", value=50, min_value=0, max_value=100)
        new_val = stat.modify(10)
        self.assertEqual(new_val, 60)

    def test_modify_lower_bound(self):
        stat = Statistic("Test", value=5, min_value=0, max_value=100)
        new_val = stat.modify(-10)
        self.assertEqual(new_val, 0)

    def test_modify_upper_bound(self):
        stat = Statistic("Test", value=95, min_value=0, max_value=100)
        new_val = stat.modify(10)
        self.assertEqual(new_val, 100)

class TestGameEntity(unittest.TestCase):
    def test_take_damage_and_is_alive(self):
        enemy = Enemy("Dummy", 10, damage_range=(2, 5))
        new_health = enemy.take_damage(3)
        self.assertEqual(new_health, 7)
        self.assertTrue(enemy.is_alive())
        new_health = enemy.take_damage(10)
        self.assertEqual(new_health, 0)
        self.assertFalse(enemy.is_alive())

class TestAbility(unittest.TestCase):
    @patch('random.random', return_value=0.0)  # always hit
    @patch('random.randint', return_value=4)   # fixed damage from randint
    def test_use_ability_hit(self, mock_randint, mock_random):
        ability = Ability("TestAbility", damage_range=(3, 7), chance_to_hit=0.9)
        char = Character("Tester", health=10)
        char.strength = Statistic("Strength", value=6)  # bonus = 6//3 = 2
        enemy = Enemy("Dummy", 10)
        result = ability.use(char, enemy)
        self.assertTrue(result)
        self.assertEqual(enemy.health, 4)  # 10 - (4+2) = 4

    @patch('random.random', return_value=0.95)  # force a miss (chance_to_hit=0.9)
    def test_use_ability_miss(self, mock_random):
        ability = Ability("TestAbility", damage_range=(3, 7), chance_to_hit=0.9)
        char = Character("Tester", health=10)
        enemy = Enemy("Dummy", 10)
        result = ability.use(char, enemy)
        self.assertFalse(result)
        self.assertEqual(enemy.health, 10)

class TestUserInputHandler(unittest.TestCase):
    @patch('builtins.input', side_effect=['invalid', 'Option1'])
    def test_get_valid_input(self, mock_input):
        options = ['Option1', 'Option2']
        result = UserInputHandler.get_valid_input("Prompt: ", options)
        self.assertEqual(result, 'Option1')

    @patch('builtins.input', side_effect=['abc', '5', '3'])
    def test_get_valid_number(self, mock_input):
        result = UserInputHandler.get_valid_number("Prompt: ", 1, 4)
        self.assertEqual(result, 3)

class TestHealthPotion(unittest.TestCase):
    @patch('random.randint', return_value=7)
    def test_use_health_potion_heals(self, mock_randint):
        char = Character("Tester", health=5)
        char.max_health = 10
        potion = HealthPotion(healing_range=(5, 10))
        result = potion.use(char)
        self.assertTrue(result)
        self.assertEqual(char.health, 10)

    def test_use_health_potion_full_health(self):
        char = Character("Tester", health=10)
        char.max_health = 10
        potion = HealthPotion(healing_range=(5, 10))
        result = potion.use(char)
        self.assertFalse(result)
        self.assertEqual(char.health, 10)

class TestCharacterHeal(unittest.TestCase):
    @patch('random.random', return_value=0.5)  # below 2/3 threshold so heal succeeds
    @patch('random.randint', return_value=6)
    def test_heal_success(self, mock_randint, mock_random):
        char = Character("Tester", health=4)
        char.max_health = 10
        result = char.heal()
        self.assertTrue(result)
        self.assertEqual(char.health, 10)

    @patch('random.random', return_value=0.8)  # above 2/3 threshold so heal fails
    def test_heal_failure(self, mock_random):
        char = Character("Tester", health=4)
        char.max_health = 10
        result = char.heal()
        self.assertFalse(result)
        self.assertEqual(char.health, 4)

class TestUseItemFromInventory(unittest.TestCase):
    @patch.object(Item, 'use', return_value=True)
    def test_use_item_success(self, mock_use):
        char = Character("Tester", health=10)
        dummy_item = Item("Dummy", "A dummy item")
        char.inventory.append(dummy_item)
        result = char.use_item_from_inventory(0)
        self.assertTrue(result)
        self.assertEqual(len(char.inventory), 0)

    def test_use_item_invalid_index(self):
        char = Character("Tester", health=10)
        result = char.use_item_from_inventory(0)
        self.assertFalse(result)

class TestEnemyAttack(unittest.TestCase):
    @patch('random.randint', return_value=3)
    def test_enemy_attack(self, mock_randint):
        char = Character("Tester", health=10)
        enemy = Enemy("Enemy", 10, damage_range=(2, 5))
        damage = enemy.attack(char)
        self.assertEqual(damage, 3)
        self.assertEqual(char.health, 7)

class TestCombat(unittest.TestCase):
    @patch('random.random', return_value=0.0)  # ensure ability always hits
    @patch('random.randint', return_value=10)  # ability deals 10 damage
    @patch('builtins.input', side_effect=['1', '1'])
    def test_combat_victory(self, mock_input, mock_randint, mock_random):
        char = Character("Tester", health=10)
        ability = Ability("Fatal Strike", damage_range=(10, 10), chance_to_hit=1.0)
        char.add_ability(ability)
        enemy = Enemy("Weak Enemy", 10, damage_range=(1, 1))
        result = combat(char, enemy)
        self.assertTrue(result)
        self.assertFalse(enemy.is_alive())

# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    # If "test" is passed as a command-line argument, run the unit tests.
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.argv.pop(1)  # Remove the "test" argument so unittest doesn't get confused.
        unittest.main()
    else:
        play_game()
