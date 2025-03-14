import random
import time

# Character class represents both player and monsters
class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

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
class Monster(Character):
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
    print("Welcome to the Tomb of the Dead!")
    player_name = input("Enter your character's name: ")

    # Initial random stage setup
    dungeon_name, min_attack, max_attack, min_health = generate_dungeon_stage()
    print(f"\nYou are about to enter the {dungeon_name}. Prepare yourself!")

    # Create player and set initial stats
    player = Character(player_name, health=100, attack=20, defense=5)

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
    while player.is_alive():
        print(f"\n--- Dungeon Level {dungeon_level} ---")
        random_event(player)
        if not combat(player, monsters):
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

    print(f"\n{player.name} has died. Game Over!")

if __name__ == "__main__":
    start_game()
