#line 190 - 195

# Game loop
def start_game():

    # Initial random stage setup
    dungeon_name, min_attack, max_attack, min_health = generate_dungeon_stage()
    print(f"\nYou are about to enter the {dungeon_name}. Prepare yourself!")
