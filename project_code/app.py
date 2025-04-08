from flask import Flask, render_template, request, redirect, url_for, session
from src.characters import WizardCat, FeralCat, ExplodingKitten
from src.entities import Enemy
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session handling


# --- ROUTES ---

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

    # Store character info
    session["character_name"] = character.name
    session["health"] = character.health
    session["max_health"] = character.max_health
    session["abilities"] = [a.name for a in character.abilities]

    # Create random enemy
    enemy = get_random_enemy()
    session["enemy_name"] = enemy.name
    session["enemy_health"] = enemy.health
    session["enemy_max_health"] = enemy.max_health

    return redirect(url_for("game_start"))


@app.route("/game")
def game_start():
    if "character_name" not in session:
        return redirect(url_for("home"))

    return render_template(
        "game.html",
        name=session["character_name"],
        health=session["health"],
        max_health=session["max_health"],
        abilities=session["abilities"],
        enemy_name=session["enemy_name"],
        enemy_health=session["enemy_health"],
        enemy_max_health=session["enemy_max_health"]
    )


@app.route("/attack", methods=["POST"])
def attack():
    selected_ability = request.form.get("ability")

    # Rebuild character from session
    name = session["character_name"]
    if name == "Wizard Cat":
        player = WizardCat()
    elif name == "Feral Cat":
        player = FeralCat()
    else:
        player = ExplodingKitten()

    player.health = session["health"]
    player.max_health = session["max_health"]

    # Rebuild enemy
    enemy = Enemy(session["enemy_name"], session["enemy_health"])

    # Use ability
    for ability in player.abilities:
        if ability.name == selected_ability:
            ability.use(player, enemy)
            break

    # Update session
    session["health"] = player.health
    session["enemy_health"] = enemy.health

    return redirect(url_for("game_start"))


# --- UTILS ---

def get_random_enemy() -> Enemy:
    enemies = [
        Enemy("Claw Bandit", 7, (2, 5)),
        Enemy("Flame Paw", 8, (3, 6)),
        Enemy("Ghost Whisker", 6, (2, 5)),
        Enemy("Halo Pouncer", 9, (3, 6))
    ]
    return random.choice(enemies)


# --- LOCAL DEV ---
if __name__ == "__main__":
    app.run(debug=True)
