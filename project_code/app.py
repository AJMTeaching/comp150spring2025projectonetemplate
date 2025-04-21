from flask import Flask, render_template, request, redirect, url_for, session
from src.characters import WizardCat, FeralCat, ExplodingKitten
from src.entities import Enemy, Item, HealthPotion
import random
import os
import json

# --- Load Location Event Text ---
def load_location_intro(location_name: str) -> str:
    folder_path = os.path.join(os.path.dirname(__file__), "location_events")
    filename = location_name.lower().replace(" ", "_") + ".json"
    filepath = os.path.join(folder_path, filename)

    if not os.path.exists(filepath):
        return "You arrive at an unknown location."

    with open(filepath, "r") as f:
        data = json.load(f)
        return data.get("intro", "This place is mysterious and silent...")


# --- UTILS ---
def get_random_enemy() -> Enemy:
    enemies = [
        Enemy("Claw Bandit", 7, (2, 5)),
        Enemy("Flame Paw", 8, (3, 6)),
        Enemy("Ghost Whisker", 6, (2, 5)),
        Enemy("Halo Pouncer", 9, (3, 6))
    ]
    return random.choice(enemies)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- ROUTES ---
@app.route("/game")
def game_start():
    if "character_name" not in session:
        return redirect(url_for("home"))

    location_intro = load_location_intro(session.get("current_location", "location_1"))

    return render_template(
        "game.html",
        name=session["character_name"],
        health=session["health"],
        max_health=session["max_health"],
        abilities=session["abilities"],
        strength=session["strength"],
        intelligence=session["intelligence"],
        inventory=session.get("inventory", []),
        enemy_name=session["enemy_name"],
        enemy_health=session["enemy_health"],
        enemy_max_health=session["enemy_max_health"],
        location_intro=location_intro
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/choose-character", methods=["POST"])
def choose_character():
    choice = request.form.get("character")
    if choice == "wizard":
        character = WizardCat()
    elif choice == "feral":
        character = FeralCat()
    elif choice == "exploding":
        character = ExplodingKitten()
    else:
        return redirect(url_for("home"))

    # Initialize session
        session["visited_locations"] = []
    session["current_location"] = "the_clawed_goblet"

    session.update({
        "character_name": character.name,
        "health": character.health,
        "max_health": character.max_health,
        "abilities": [a.name for a in character.abilities],
        "inventory": ["Health Potion"],
        "strength": character.strength.value,
        "intelligence": character.intelligence.value,
        "locations_visited": 0
    })

    enemy = get_random_enemy()
    session.update({
        "enemy_name": enemy.name,
        "enemy_health": enemy.health,
        "enemy_max_health": enemy.max_health
    })

    return redirect(url_for("game_start"))

@app.route("/game")
def game_start():
    if "character_name" not in session:
        return redirect(url_for("home"))

    return render_template("game.html",
        name=session["character_name"],
        health=session["health"],
        max_health=session["max_health"],
        abilities=session["abilities"],
        strength=session["strength"],
        intelligence=session["intelligence"],
        inventory=session.get("inventory", []),
        enemy_name=session["enemy_name"],
        enemy_health=session["enemy_health"],
        enemy_max_health=session["enemy_max_health"]
    )

@app.route("/attack", methods=["POST"])
def attack():
    data = request.get_json()
    selected_ability = data.get("ability")

    player = _rebuild_player_from_session()
    enemy = Enemy(session["enemy_name"], int(session["enemy_health"]))

    message = "Something went wrong."
    for ability in player.abilities:
        if ability.name == selected_ability:
            success = ability.use(player, enemy)
            message = f"{player.name} used {ability.name} and dealt damage!" if success else f"{player.name} used {ability.name} but missed!"
            break

    session["health"] = player.health
    session["enemy_health"] = enemy.health

    if enemy.health <= 0:
        session["locations_visited"] += 1
        if session["locations_visited"] >= 3:
            final_boss = Enemy("Barking Kitten War General", 14, (4, 7))
            session.update({
                "enemy_name": final_boss.name,
                "enemy_health": final_boss.health,
                "enemy_max_health": final_boss.max_health
            })
            message += "\nYou have defeated all enemies! Prepare for the final battle!"
        else:
            new_enemy = get_random_enemy()
            session.update({
                "enemy_name": new_enemy.name,
                "enemy_health": new_enemy.health,
                "enemy_max_health": new_enemy.max_health,
                "health": min(session["health"] + 3, session["max_health"])
            })
            message += "\nEnemy defeated! You move on to the next zone and regain 3 HP."

    return {
        "player_health": player.health,
        "player_max_health": player.max_health,
        "enemy_health": session["enemy_health"],
        "enemy_max_health": session["enemy_max_health"],
        "message": message
    }

@app.route("/heal", methods=["POST"])
def heal():
    player = _rebuild_player_from_session()
    success = player.heal()
    session["health"] = player.health

    return {
        "player_health": player.health,
        "player_max_health": player.max_health,
        "message": f"{player.name} healed successfully!" if success else f"{player.name} tried to heal but failed!"
    }

@app.route("/use-item", methods=["POST"])
def use_item():
    inventory = session.get("inventory", [])
    player = _rebuild_player_from_session()

    if "Health Potion" in inventory:
        potion = HealthPotion()
        potion.use(player)
        inventory.remove("Health Potion")
        session.update({
            "inventory": inventory,
            "health": player.health
        })
        message = f"{player.name} used a Health Potion!"
    else:
        message = "No Health Potions left!"

    return {
        "player_health": player.health,
        "player_max_health": player.max_health,
        "message": message
    }

# --- UTILITY REBUILDER ---
def _rebuild_player_from_session():
    name = session["character_name"]
    if name == "Wizard Cat":
        player = WizardCat()
    elif name == "Feral Cat":
        player = FeralCat()
    else:
        player = ExplodingKitten()

    player.health = int(session["health"])
    player.max_health = int(session["max_health"])
    player.strength.value = session["strength"]
    player.intelligence.value = session["intelligence"]
    return player

# --- DEMO ROUTES ---
@app.route("/increment", methods=["POST"])
def increment():
    session["count"] = session.get("count", 0) + 1
    return {"count": session["count"]}

@app.route("/flip_case", methods=["POST"])
def flip_case():
    data = request.get_json()
    text = data.get("text", "")
    flipped = ''.join(c.upper() if c.islower() else c.lower() for c in text)
    return {"flipped_text": flipped}

# --- DEV ENTRY POINT ---
if __name__ == "__main__":
    app.run(debug=True)
