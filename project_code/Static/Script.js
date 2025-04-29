// --- Combat Action Handlers ---
function useAbility(abilityName) {
  playSound("attack-sound");
  sendAction('/attack', { ability: abilityName });
}

function heal() {
  playSound("heal-sound");
  sendAction('/heal');
}

function useItem() {
  playSound("item-sound");
  sendAction('/use-item');
}

function playSound(id) {
  const sound = document.getElementById(id);
  if (sound) {
    sound.currentTime = 0;
    sound.play();
  }
}

// --- Shared Send + Response Logic ---
function sendAction(endpoint, payload = {}) {
  disableButtons();
  axios.post(endpoint, payload)
    .then(response => {
      const data = response.data;

      // Check redirect and play end-of-game sounds
      if (data.redirect) {
        if (data.redirect.includes("victory")) playSound("victory-sound");
        if (data.redirect.includes("defeated")) playSound("defeat-sound");

        showCombatLog(data.message || "Redirecting...");
        setTimeout(() => window.location.href = data.redirect, 1500);
      } else {
        // Check if enemy dealt damage
        if (data.message?.includes("counterattacked")) {
          playSound("damage-sound");
        }
        updateGameState(data);
      }
    })
    .catch(console.error)
    .finally(enableButtons);
}

// --- Update Game State ---
function updateGameState(data) {
  animateHealthUpdate("player-health", data.player_health, data.player_max_health);
  animateHealthUpdate("enemy-health", data.enemy_health, data.enemy_max_health);

  const logBox = document.getElementById("log-messages");
  const lines = (data.message || "[No message]").split("\n");

  const formatted = lines.map(line => {
    if (line.includes("Max Health increased")) return `❤️ ${line}`;
    if (line.includes("increased by 1")) return `✨ ${line}`;
    if (line.includes("Health Potion")) return `🧪 ${line}`;
    if (line.includes("Final Boss")) return `🏆 ${line}`;
    if (line.includes("Zone cleared")) return `🌍 ${line}`;
    return `🗡️ ${line}`;
  });

  logBox.textContent = formatted.join("\n") + "\n" + logBox.textContent;
  logBox.scrollTop = 0;
}

// --- Animate Health Changes ---
function animateHealthUpdate(id, hp, maxHp) {
  const elem = document.getElementById(id);
  elem.textContent = `${hp} / ${maxHp}`;
  elem.classList.remove("flash-hit");
  void elem.offsetWidth;
  elem.classList.add("flash-hit");
}

// --- Combat Log Display ---
function showCombatLog(message) {
  const logBox = document.getElementById("log-messages");
  const entry = document.createElement("div");
  entry.className = "fade-log";
  entry.textContent = message;
  logBox.prepend(entry);
  logBox.scrollTop = 0;
}

// --- Button Control ---
function disableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = true);
}

function enableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = false);
}
