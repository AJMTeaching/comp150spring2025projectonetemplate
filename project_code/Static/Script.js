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

  animateHealthUpdate("player-health", data.player_health, data.player_max_health);
  animateHealthUpdate("enemy-health", data.enemy_health, data.enemy_max_health);

  showCombatLog(data.message);
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
