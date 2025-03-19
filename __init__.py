import random
import time

# Character class represents both player and monsters
class Character:
    def __init__(self, name, attack, health, mana, defense):
        self.name = name
        self.attack = attack
        self.health = health
        self.mana = mana
        self.defense = defense

    def __str__(self):
        return f"{self.name}: Attack={self.attack}, Health={self.health}, Mana={self.mana},defense={self.defense}"


class Swordsman(Character):
    def __init__(self, name):
        # Swordsman has higher attack, lower health, and no mana
        super().__init__(name, attack=20, health=50, mana=0,defense=100)


class Mage(Character):
    def __init__(self, name):
        # Mage has lower attack, higher health, and starting mana of 5
        super().__init__(name, attack=10, health=80, mana=5,defense=100)
        self.initial_mana = 5  # Track the starting mana

    def defeat_monster(self):
        # Each time a monster is defeated, increase mana by 5
        self.mana += 5

    def __str__(self):
        return f"{self.name}: Attack={self.attack}, Health={self.health}, Mana={self.mana}"

def choose_character():
    print("Welcome to the game!")
    print("Choose your character class:")
    print("1. Swordsman (Higher attack, lower health, no mana)")
    print("2. Mage (Lower attack, higher health, starting mana of 5 that increases with each monster defeated)")

    choice = input("Enter the number of your choice (1 or 2): ")

    if choice == "1":
        name = input("Enter the name of your Swordsman: ")
        character = Swordsman(name)
        print(f"\nYou have chosen {character.name}, the Swordsman!")
        print(character)
    elif choice == "2":
        name = input("Enter the name of your Mage: ")
        character = Mage(name)
        print(f"\nYou have chosen {character.name}, the Mage!")
        print(character)
    else:
        print("Invalid choice. Please choose either 1 or 2.")
        return choose_character()  # Restart the choice prompt if invalid input is given

    return character


# Starting the game and choosing a character
chosen_character = choose_character()

def equip_armor(self, defense_boost):
        """Equips armor, increasing defense."""
        self.defense += defense_boost
        print(f"{self.name} equipped armor! Defense increased to {self.defense:.2f}.")

def check_chest(self):
        """Checks a chest for armor."""
        if random.random() < 0.45:  # 45% chance of finding armor
            defense_boost = random.randint(10, 50)  # Random defense boost
            self.equip_armor(defense_boost)
        else:
            print(f"{self.name} found nothing in the chest.")

def attack(self, target, damage):
        """Attacks another character."""
        actual_damage = damage
        self.target=target
        self.target=Monster

        if self.defense == 0: #damage boost if no armor
                actual_damage *= 1.03

        if target.defense > 0:
            actual_damage = max(0, actual_damage - (actual_damage * (target.defense / 100))) # apply damage reduction.
            target.defense = max(0, target.defense - 5) # reduce defense
            print(f"{self.name} attacks {target.name} for {actual_damage:.2f} damage (Defense reduced).")
        else:
            print(f"{self.name} attacks {target.name} for {actual_damage:.2f} damage (No defense).")

        target.health -= actual_damage
        target.health = max(0, target.health)  # Ensure health doesn't go below 0
        print(f"{target.name}'s health: {target.health:.2f}")

def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage

def is_alive(self):
        return self.health > 0

def attack_enemy(self, enemy):
        damage = random.randint(1, self.attack)
        actual_damage = enemy.take_damage(damage)
        return actual_damage

# Monster class inherits from Character class
class Monster:
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)

    def attack_player(self, player):
        damage = random.randint(1, self.attack)
        actual_damage = player.take_damage(damage)
        return actual_damage

# Event-based random dungeon generation
def generate_dungeon_stage():
    # Random dungeon stage factor (can affect difficulty)
    stage_value = random.randint(1, 10)
    print(f"Stage Value: {stage_value}")
    
    if stage_value <= 3:
        return "Goblin Lair", 3, 5, 8  # Monster, Min Attack, Max Attack, Min Health
    elif stage_value <= 7:
        return "Cursed Tomb", 5, 10, 12
    else:
        return "Dragon's Den", 8, 15, 20

# Printing status of the game
def print_status(player, monsters):
    print(f"\n{player.name} - Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}")
    for monster in monsters:
        print(f"{monster.name} - Health: {monster.health}, Attack: {monster.attack}, Defense: {monster.defense}")
    print("\n")

# Combat system between player and monsters
def combat(player, monsters):
    # Start combat
    while player.is_alive() and any(monster.is_alive() for monster in monsters):
        print_status(player, monsters)

        # Player's turn to attack
        print(f"{player.name}'s turn!")
        target_idx = int(input("Choose a monster to attack (1 for first, 2 for second, etc.): ")) - 1
        if target_idx >= 0 and target_idx < len(monsters) and monsters[target_idx].is_alive():
            damage = player.attack_enemy(monsters[target_idx])
            print(f"{player.name} attacks {monsters[target_idx].name} for {damage} damage!")
        else:
            print("Invalid target! No attack made.")
        
        # Monsters' turn to attack
        if any(monster.is_alive() for monster in monsters):
            time.sleep(1)  # Dramatic pause
            print("\nThe monsters are attacking!")
            for monster in monsters:
                if monster.is_alive():
                    damage = monster.attack_player(player)
                    print(f"{monster.name} attacks you for {damage} damage!")

        # Check if player is still alive
        if not player.is_alive():
            print(f"\nGame Over! {player.name} has fallen in battle.")
            return False

    if not any(monster.is_alive() for monster in monsters):
        print("\nYou have defeated all the monsters!")
        return True

# Random event in the dungeon (treasure, trap, etc.)
def random_event(player):
    event = random.choice(["treasure", "trap", "nothing"])
    if event == "treasure":
        treasure_value = random.randint(1, 5)
        print(f"\nYou find a treasure chest! You gain {treasure_value} health and attack boost.")
        player.health += treasure_value
        player.attack += treasure_value
    elif event == "trap":
        trap_damage = random.randint(5, 15)
        print(f"\nYou triggered a trap! You take {trap_damage} damage.")
        player.take_damage(trap_damage)
    else:
        print("\nYou walk through the dungeon without encountering anything.")

# Game loop
def start_game():

    # Initial random stage setup
    dungeon_name, min_attack, max_attack, min_health = generate_dungeon_stage()
    print(f"\nYou are about to enter the {dungeon_name}. Prepare yourself!")

    # Prepare monsters for this dungeon
    monster_count = random.randint(3, 6)
    monsters = []
    for i in range(monster_count):
        monster_name = f"Monster-{i+1}"
        monster_attack = random.randint(min_attack, max_attack)
        monster_health = random.randint(min_health, min_health + 10)
        monster_defense = random.randint(2, 5)
        monsters.append(Monster(monster_name, monster_health, monster_attack, monster_defense))

    # Game loop
    dungeon_level = 1
    while chosen_character.is_alive():
        print(f"\n--- Dungeon Level {dungeon_level} ---")
        random_event(Character)
        if not combat(Character, monsters):
            break

        # Proceed to next dungeon level
        dungeon_level += 1
        monsters = []  # Reset monsters after level

        # Re-generate new monsters for next level
        monster_count = random.randint(3, 6)
        for i in range(monster_count):
            monster_name = f"Monster-{i+1}"
            monster_attack = random.randint(min_attack, max_attack)
            monster_health = random.randint(min_health, min_health + 10)
            monster_defense = random.randint(2, 5)
            monsters.append(Monster(monster_name, monster_health, monster_attack, monster_defense))

    print(f"\n{Character.name} has died. Game Over!")

if __name__ == "__main__":
    start_game()
