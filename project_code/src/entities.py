import random
from typing import List
from abc import ABC, abstractmethod


# --- STATISTIC ---
class Statistic:
    def __init__(self, name: str, value: int = 0, min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def modify(self, amount: int) -> int:
        self.value = max(self.min_value, min(self.max_value, self.value + amount))
        return self.value


# --- BASE GAME ENTITY ---
class GameEntity(ABC):
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
        self.max_health = health

    def take_damage(self, amount: int) -> int:
        self.health = max(0, self.health - amount)
        return self.health

    def is_alive(self) -> bool:
        return self.health > 0


# --- ABILITY ---
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
            target.take_damage(damage)
            return True
        return False


# --- ITEM ---
class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def use(self, character: 'Character') -> bool:
        return True


# --- CHARACTER ---
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
            self.health = min(self.max_health, self.health + heal_amount)
            return True
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


# --- ENEMY ---
class Enemy(GameEntity):
    def __init__(self, name: str, health: int, damage_range: tuple = (2, 5)):
        super().__init__(name, health)
        self.damage_range = damage_range

    def attack(self, target: Character) -> int:
        damage = random.randint(*self.damage_range)
        target.take_damage(damage)
        return damage


# --- HEALTH POTION ---
class HealthPotion(Item):
    def __init__(self, healing_range: tuple = (5, 10)):
        super().__init__(name="Health Potion", description="Restores health")
        self.healing_range = healing_range

    def use(self, character: 'Character') -> bool:
        if character.health < character.max_health:
            heal_amount = random.randint(*self.healing_range)
            character.health = min(character.max_health, character.health + heal_amount)
            return True
        return False
