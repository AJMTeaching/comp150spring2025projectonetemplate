// --- Combat Action Handlers ---
function useAbility(abilityName) {
  disableButtons();
  axios.post('/attack', { ability: abilityName })
    .then(response => {
      if (response.data.redirect) {
        showCombatLog(response.data.message || "Redirecting...");
        setTimeout(() => window.location.href = response.data.redirect, 1500);
      } else {
        updateGameState(response);
      }
    })
    .catch(console.error)
    .finally(enableButtons);
}

function heal() {
  disableButtons();
  axios.post('/heal')
    .then(updateGameState)
    .catch(console.error)
    .finally(enableButtons);
}

function useItem() {
  disableButtons();
  axios.post('/use-item')
    .then(updateGameState)
    .catch(console.error)
    .finally(enableButtons);
}

// --- Shared Update Function ---
function updateGameState(response) {
  const data = response.data;

  // Update health bars
  document.getElementById("player-health").textContent =
    `${data.player_health} / ${data.player_max_health}`;
  document.getElementById("enemy-health").textContent =
    `${data.enemy_health} / ${data.enemy_max_health}`;

  // Format and display combat log
  const logBox = document.getElementById("log-messages");
  const messages = (data.message || "[No message]").split("\n");

  const formatted = messages.map(line => {
    if (line.includes("Max Health increased")) {
      return `❤️ ${line}`;
    } else if (line.includes("increased by 1")) {
      return `✨ ${line}`;
    } else if (line.includes("Health Potion")) {
      return `🧪 ${line}`;
    } else if (line.includes("Final Boss")) {
      return `🏆 ${line}`;
    } else if (line.includes("Zone cleared")) {
      return `🌍 ${line}`;
    }
    return line;
  });

  logBox.textContent = formatted.join("\n") + "\n" + logBox.textContent;
  logBox.scrollTop = 0;
}


// --- Animate Health Changes ---
function animateHealthUpdate(id, hp, maxHp) {
  const elem = document.getElementById(id);
  elem.textContent = `${hp} / ${maxHp}`;
  elem.classList.remove("flash-hit");
  void elem.offsetWidth; // Force reflow
  elem.classList.add("flash-hit");
}

// --- Log Message Display ---
function showCombatLog(msg) {
  const logBox = document.getElementById("log-messages");
  const entry = document.createElement("div");
  entry.className = "fade-log";
  entry.textContent = msg || "[No message]";
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
