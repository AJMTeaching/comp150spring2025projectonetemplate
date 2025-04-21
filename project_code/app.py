from flask import Flask, render_template, request, redirect, url_for, session
from src.characters import WizardCat, FeralCat, ExplodingKitten
from src.entities import Enemy, HealthPotion
import random, os, json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- Location Data ---
LOCATIONS = [
    "The Clawed Goblet",
    "Felis Infernum",
    "The Witherwild Thicket",
    "The Purrgola",
    "Felis Elysium"
]

# --- Load Location Description ---
def load_location_intro(location_name: str) -> str:
    folder_path = os.path.join(os.path.dirname(__file__), "location_events")
    filename = location_name.lower().replace(" ", "_") + ".json"
    filepath = os.path.join(folder_path, filename)
    if not os.path.exists(filepath):
        return "You arrive at an unknown location."
    with open(filepath, "r") as f:
        data = json.load(f)
        return data.get("intro", "This place is mysterious and silent...")

# --- Enemys  ---
def get_enemy_for_location(location: str) -> Enemy:
    return random.choice(LOCATION_ENEMIES.get(location, [Enemy("Unknown Puppy", 6, (2, 4))]))
LOCATION_ENEMIES = {
    "The Clawed Goblet": [
        Enemy("Claw Bandit", 7, (2, 5)),
        Enemy("Goblet Growler", 8, (3, 6))
    ],
    "Felis Infernum": [
        Enemy("Flame Paw", 8, (3, 6)),
        Enemy("Inferno Pup", 9, (4, 7))
    ],
    "The Witherwild Thicket": [
        Enemy("Ghost Whisker", 6, (2, 5)),
        Enemy("Thicket Howler", 7, (3, 5))
    ],
    "The Purrgola": [
        Enemy("Sunnapper", 6, (2, 4)),
        Enemy("Purring Menace", 7, (2, 5))
    ],
    "Felis Elysium": [
        Enemy("Halo Pouncer", 9, (3, 6)),
        Enemy("Blessed Barker", 10, (4, 6))
    ]
    }  

# --- Home & Character Select ---
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

    session.update({
        "character_name": character.name,
        "health": character.health,
        "max_health": character.max_health,
        "abilities": [{"name": a.name, "description": a.description} for a in character.abilities],
        "inventory": ["Health Potion"],
        "strength": character.strength.value,
        "intelligence": character.intelligence.value,
        "visited_locations": [],
        "locations_visited": 0
    })

    return redirect(url_for("select_location"))

# --- Location Select ---
@app.route("/select-location")
def select_location():
    visited = session.get("visited_locations", [])
    unvisited = [loc for loc in LOCATIONS if loc not in visited]

    if not unvisited or len(visited) >= 3:
        session.update({
            "enemy_name": "Barking Kitten War General",
            "enemy_health": 14,
            "enemy_max_health": 14
        })
        return redirect(url_for("game"))

    return render_template("select_location.html", locations=unvisited)

@app.route("/enter-location", methods=["POST"])
def enter_location():
    location = request.form.get("location")
    session["current_location"] = location
    session["visited_locations"].append(location)

    enemy = get_enemy_for_location(location)
    session.update({
        "enemy_name": enemy.name,
        "enemy_health": enemy.health,
        "enemy_max_health": enemy.max_health
    })
    return redirect(url_for("game"))

# --- Main Game View ---
@app.route("/game")
def game():
    if "character_name" not in session:
        return redirect(url_for("home"))

    location_intro = load_location_intro(session.get("current_location", "unknown"))
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
        enemy_max_health=session["enemy_max_health"],
        location_intro=location_intro
    )

# --- Combat Handler ---
@app.route("/attack", methods=["POST"])
def attack():
    data = request.get_json()
    selected_ability = data.get("ability")
    player = _rebuild_player_from_session()
    enemy = Enemy(session["enemy_name"], session["enemy_health"])
    inventory = session.get("inventory", [])

    message = "Something went wrong."
    for ability in player.abilities:
        if ability.name == selected_ability:
            success = ability.use(player, enemy)
            message = f"{player.name} used {ability.name} and dealt damage!" if success else f"{player.name} used {ability.name} but missed!"
            break

    session["enemy_health"] = enemy.health

    # 🧱 Check for enemy defeat before they get to counterattack
    if not enemy.is_alive():
        session["locations_visited"] += 1
        loot_messages = []

        if random.random() < 0.5:
            inventory.append("Health Potion")
            loot_messages.append("You found a Health Potion!")

        if random.random() < 0.3:
            stat = random.choice(["strength", "intelligence"])
            session[stat] += 1
            loot_messages.append(f"✨ {stat.capitalize()} increased by 1!")

        session["max_health"] += 1
        session["health"] = session["max_health"]
        session["inventory"] = inventory
        loot_messages.append("❤️ Max Health increased by 1!")

        if session["enemy_name"] == "Barking Kitten War General":
            return {
                "redirect": url_for("victory"),
                "message": "You defeated the Final Boss! 🏆\n" + "\n".join(loot_messages)
            }

        return {
            "redirect": url_for("select_location"),
            "message": "🌍 Zone cleared!\n" + "\n".join(loot_messages)
        }

    # 🐶 Enemy counterattack happens here
    damage = enemy.attack(player)
    message += f"\n{enemy.name} counterattacked and dealt {damage} damage to {player.name}!"

    session["health"] = player.health

    if not player.is_alive():
        return {
            "redirect": url_for("defeated"),
            "message": f"{player.name} has fallen in battle..."
        }

    return {
        "player_health": player.health,
        "player_max_health": player.max_health,
        "enemy_health": enemy.health,
        "enemy_max_health": enemy.max_health,
        "message": message
    }

# --- Healing ---
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

# --- Item Use ---
@app.route("/use-item", methods=["POST"])
def use_item():
    inventory = session.get("inventory", [])
    player = _rebuild_player_from_session()
    if "Health Potion" in inventory:
        HealthPotion().use(player)
        inventory.remove("Health Potion")
        session.update({"inventory": inventory, "health": player.health})
        return {
            "player_health": player.health,
            "player_max_health": player.max_health,
            "message": f"{player.name} used a Health Potion!"
        }
    return {
        "player_health": player.health,
        "player_max_health": player.max_health,
        "message": "No Health Potions left!"
    }

# --- Victory & Defeat Screens ---
@app.route("/victory")
def victory():
    return render_template("victory.html",
        name=session.get("character_name", "Unknown Cat"),
        visited_locations=session.get("visited_locations", []),
        strength=session.get("strength", 0),
        intelligence=session.get("intelligence", 0),
        inventory=session.get("inventory", [])
    )

@app.route("/defeated")
def defeated():
    return render_template("defeated.html", name=session.get("character_name", "Unknown Cat"))

# --- Reset Session ---
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

# --- Debug/Demo Routes ---
@app.route("/increment", methods=["POST"])
def increment():
    session["count"] = session.get("count", 0) + 1
    return {"count": session["count"]}

@app.route("/flip_case", methods=["POST"])
def flip_case():
    data = request.get_json()
    flipped = ''.join(c.upper() if c.islower() else c.lower() for c in data.get("text", ""))
    return {"flipped_text": flipped}

# --- Reconstruct Character From Session ---
def _rebuild_player_from_session():
    if session["character_name"] == "Wizard Cat":
        p = WizardCat()
    elif session["character_name"] == "Feral Cat":
        p = FeralCat()
    else:
        p = ExplodingKitten()
    p.health = session["health"]
    p.max_health = session["max_health"]
    p.strength.value = session["strength"]
    p.intelligence.value = session["intelligence"]
    return p

if __name__ == "__main__":
    app.run(debug=True)
