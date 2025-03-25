import json
import random
from typing import List, Dict, Optional
from enum import Enum
from abc import ABC, abstractmethod

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
        """Modify statistic and return the new value"""
        self.value = max(self.min_value, min(self.max_value, self.value + amount))
        return self.value

# --- GAME ENTITY BASE CLASS ---
class GameEntity(ABC):
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
        self.max_health = health
    
    def take_damage(self, amount: int) -> int:
        """Take damage and return remaining health"""
        self.health = max(0, self.health - amount)
        print(f"{self.name} took {amount} damage! Remaining Health: {self.health}")
        return self.health
    
    def is_alive(self) -> bool:
        """Check if entity is still alive"""
        return self.health > 0

# --- ABILITY CLASS ---
class Ability:
    def __init__(self, name: str, damage_range: tuple = (3, 7), chance_to_hit: float = 0.9):
        self.name = name
        self.damage_range = damage_range
        self.chance_to_hit = chance_to_hit
    
    def use(self, user: 'Character', target: GameEntity) -> bool:
        """Use ability on target, return True if hit, False if missed"""
        if random.random() <= self.chance_to_hit:
            damage = random.randint(*self.damage_range)
            # Add strength bonus for physical abilities
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
        """Get valid input from user based on options"""
        options_lower = [opt.lower() for opt in options]
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in options_lower:
                return options[options_lower.index(user_input)]
            print(f"Invalid input! Please choose from: {', '.join(options)}")

    @staticmethod
    def get_valid_number(prompt: str, min_val: int, max_val: int) -> int:
        """Get valid number from user within range"""
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
    def __init__(self, name: str, price: int, description: str):
        self.name = name
        self.price = price
        self.description = description
    
    def use(self, character: 'Character') -> bool:
        """Use item on character, return True if successful"""
        print(f"{character.name} used {self.name}!")
        return True

class HealthPotion(Item):
    def __init__(self, healing_range: tuple = (5, 10)):
        super().__init__(
            name="Health Potion", 
            price=3, 
            description="Restores health"
        )
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

class StatBoost(Item):
    def __init__(self, stat_name: str, boost_amount: int = 2):
        super().__init__(
            name=f"{stat_name} Boost", 
            price=5, 
            description=f"Increases {stat_name} by {boost_amount}"
        )
        self.stat_name = stat_name.lower()
        self.boost_amount = boost_amount
    
    def use(self, character: 'Character') -> bool:
        if hasattr(character, self.stat_name):
            stat = getattr(character, self.stat_name)
            if isinstance(stat, Statistic):
                old_value = stat.value
                new_value = stat.modify(self.boost_amount)
                print(f"{character.name}'s {self.stat_name} increased from {old_value} to {new_value}!")
                return True
        print(f"{character.name} cannot use this item!")
        return False

# --- CHARACTER CLASSES ---
class Character(GameEntity):
    def __init__(self, name: str, health: int = 10, coins: int = 0):
        super().__init__(name, health)
        self.inventory: List[Item] = []
        self.strength = Statistic("Strength", value=5)
        self.intelligence = Statistic("Intelligence", value=5)
        self.abilities: List[Ability] = []
        self.coins = coins

    def heal(self) -> bool:
        """Attempt to heal, with 2/3 chance of success"""
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
        """Add ability to character"""
        self.abilities.append(ability)

    def earn_coins(self, amount: int) -> int:
        """Earn coins and return new total"""
        self.coins += amount
        print(f"{self.name} earned {amount} coins! Total: {self.coins}")
        return self.coins

    def spend_coins(self, amount: int) -> bool:
        """Spend coins, return True if successful"""
        if self.coins >= amount:
            self.coins -= amount
            print(f"{self.name} spent {amount} coins. Remaining: {self.coins}")
            return True
        else:
            print("Not enough coins!")
            return False
    
    def use_item_from_inventory(self, item_index: int) -> bool:
        """Use item from inventory at given index"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if item.use(self):
                self.inventory.pop(item_index)
                return True
        return False

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12, coins=5)
        self.intelligence.value = 8  # Higher intelligence
        self.add_ability(Ability("Fireball", damage_range=(4, 8)))
        self.add_ability(Ability("Magic Shield", damage_range=(2, 5)))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15, coins=3)
        self.strength.value = 8  # Higher strength
        self.add_ability(Ability("Forsaken Furball", damage_range=(5, 9)))
        self.add_ability(Ability("Cowardice", damage_range=(3, 6)))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10, coins=7)
        # Balanced stats
        self.add_ability(Ability("Nuclear Reactivity", damage_range=(4, 10)))
        self.add_ability(Ability("Controlled Explosion", damage_range=(3, 7)))

# --- ENEMY CLASS ---
class Enemy(GameEntity):
    def __init__(self, name: str, health: int, damage_range: tuple = (2, 5), coins_reward: int = 5):
        super().__init__(name, health)
        self.damage_range = damage_range
        self.coins_reward = coins_reward
    
    def attack(self, target: Character) -> int:
        """Attack target and return damage dealt"""
        damage = random.randint(*self.damage_range)
        print(f"{self.name} attacks for {damage} damage!")
        target.take_damage(damage)
        return damage

# --- COMBAT SYSTEM ---
def combat(player: Character, enemy: Enemy) -> bool:
    """Run combat between player and enemy, return True if player wins"""
    print(f"{player.name} engages in battle with {enemy.name}!")
    
    # Combat loop
    while player.is_alive() and enemy.is_alive():
        # Player's turn
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
            # Use ability
            print("Choose an ability:")
            for idx, ability in enumerate(player.abilities):
                print(f"{idx + 1}. {ability.name}")
            choice = UserInputHandler.get_valid_number("Enter ability number: ", 1, len(player.abilities)) - 1
            player.abilities[choice].use(player, enemy)
        elif action == 2:
            # Heal
            player.heal()
        elif action == 3 and player.inventory:
            # Use item
            print("Choose an item:")
            for idx, item in enumerate(player.inventory):
                print(f"{idx + 1}. {item.name} - {item.description}")
            choice = UserInputHandler.get_valid_number("Enter item number: ", 1, len(player.inventory)) - 1
            player.use_item_from_inventory(choice)

        # Check if enemy was defeated
        if not enemy.is_alive():
            print(f"{enemy.name} is defeated!")
            reward = enemy.coins_reward
            player.earn_coins(reward)
            print(f"You found {reward} coins!")
            return True

        # Enemy's turn
        print(f"\n{enemy.name}'s turn! Health: {enemy.health}")
        enemy.attack(player)
        
        # Check if player was defeated
        if not player.is_alive():
            print(f"{player.name} has been defeated...")
            return False
    
    # This should never be reached, but just in case
    return player.is_alive()

# --- SHOP SYSTEM ---
class Shop:
    def __init__(self):
        self.items: Dict[str, Item] = {
            "Health Potion": HealthPotion(),
            "Strength Boost": StatBoost("Strength"),
            "Intelligence Boost": StatBoost("Intelligence")
        }

    def display_items(self) -> None:
        """Display available items in shop"""
        print("Welcome to the Shop! Available items:")
        for name, item in self.items.items():
            print(f"{name}: {item.price} coins - {item.description}")

    def purchase(self, player: Character) -> bool:
        """Handle purchase transaction, return True if purchase made"""
        self.display_items()
        options = list(self.items.keys()) + ["exit"]
        choice = UserInputHandler.get_valid_input("What would you like to buy? (Enter item name or 'exit' to leave): ", options)
        
        if choice == "exit":
            return False
            
        item = self.items[choice]
        if player.spend_coins(item.price):
            player.inventory.append(item)
            print(f"{player.name} purchased {choice}!")
            return True
        return False

# --- GAME STATES ---
class GameState:
    def __init__(self):
        self.player: Optional[Character] = None
        self.locations_visited = 0
        self.max_locations = 3
        self.shop = Shop()
    
    def visit_shop(self) -> None:
        """Visit shop and handle purchases"""
        print("\nYou stumble upon a mysterious shop...")
        while True:
            choice = UserInputHandler.get_valid_input("Do you want to enter? (yes/no): ", ["yes", "no"])
            if choice.lower() == "yes":
                made_purchase = self.shop.purchase(self.player)
                if not made_purchase:
                    break
            else:
                break

# --- LOCATION AND ENEMY GENERATION ---
def get_location_enemy(location: str) -> Enemy:
    """Get appropriate enemy for location"""
    if location == "The Clawed Goblet":
        return Enemy("Claw Bandit", 7, damage_range=(2, 5), coins_reward=4)
    elif location == "Felis Infernum":
        return Enemy("Flame Paw", 8, damage_range=(3, 6), coins_reward=6)
    elif location == "The Witherwild Thicket":
        return Enemy("Ghost Whisker", 6, damage_range=(2, 5), coins_reward=3)
    elif location == "The Purrgola":
        return Enemy("Sunning Saboteur", 7, damage_range=(2, 4), coins_reward=5)
    elif location == "Felis Elysium":
        return Enemy("Halo Pouncer", 9, damage_range=(3, 6), coins_reward=7)
    else:
        # Default enemy if location not recognized
        return Enemy("Mysterious Cat", 7, damage_range=(2, 5), coins_reward=5)

# --- GAME LOGIC ---
def choose_character() -> Character:
    """Let user choose character"""
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
    """Choose location to explore, showing which have been visited"""
    print("Choose a location to explore:")
    for idx, loc in enumerate(locations, 1):
        status = " (visited)" if loc in visited else ""
        print(f"{idx}. {loc}{status}")
    choice = UserInputHandler.get_valid_number("Enter location number: ", 1, len(locations)) - 1
    return locations[choice]

def play_game() -> None:
    """Main game loop"""
    print("Welcome to Exploding Kittens: The RPG!")
    print("The Kitten Forest Forces have always defended their territory with precision and finesse.")
    print("However, there has been a security breach detected on the borders!")
    print("You are a new recruit, ready to serve. The whole colony is on lockdown and Sergeant Barking Kitten takes you under his paw!")
    print("With a tiny meow, he demands you: >\"There's an intruder in our ranks, rookie! If you want to survive, you need to learn some skills fast!\"")
    print("Your mission is clear: Find the Intruder and eliminate the threat!\n")

    # Setup game state
    game_state = GameState()
    game_state.player = choose_character()
    print(f"You have chosen: {game_state.player.name}\n")
    
    # Starting items
    game_state.player.inventory.append(HealthPotion())
    print(f"You received a Health Potion to start your journey!")

    # Available locations
    locations = ["The Clawed Goblet", "Felis Infernum", "The Witherwild Thicket", "The Purrgola", "Felis Elysium"]
    visited_locations = []
    
    # Main game loop
    while game_state.locations_visited < game_state.max_locations and game_state.player.is_alive():
        # Choose location
        location = choose_location(locations, visited_locations)
        visited_locations.append(location)
        game_state.locations_visited += 1
        
        print(f"\nExploring {location}...")
        
        # Create enemy for location
        enemy = get_location_enemy(location)
        
        # Combat
        victory = combat(game_state.player, enemy)
        if victory:
            game_state.player.max_health += 1
            game_state.player.health = game_state.player.max_health
            print(f"{game_state.player.name} has grown stronger! Max health is now {game_state.player.max_health}.")
            
            # Random chance for shop to appear
            if random.random() < 0.7:  # 70% chance for shop
                game_state.visit_shop()
        else:
            print("Game Over! You were defeated!")
            return
    
    # Final boss battle
    if game_state.player.is_alive():
        print("\nFinal Battle: The Barking Kitten War General appears from the shadows!")
        final_boss = Enemy("Barking Kitten War General", 14, damage_range=(4, 7), coins_reward=10)
        
        # Final shop visit before boss
        print("Before facing the War General, a merchant tugs at your fur...")
        game_state.visit_shop()
        
        if combat(game_state.player, final_boss):
            print("Congratulations! You defeated the Barking Kitten War General.")
            print("The Kitten Military Forces are saved, and you become a hero among cats!")
        else:
            print("Game Over! You were defeated by the Barking Kitten War General. Rest in Peace, soldier.")

# --- START GAME ---
if __name__ == "__main__":
    play_game()