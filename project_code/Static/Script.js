// --- Game Ability Attack ---
function useAbility(abilityName) {
  disableButtons();
  axios.post('/attack', { ability: abilityName })
    .then(response => {
      if (response.data.redirect) {
        window.location.href = response.data.redirect;
      } else {
        updateGameState(response);
      }
    })
    .catch(console.error)
    .finally(enableButtons);
}

// --- Heal Action ---
function heal() {
  disableButtons();
  axios.post('/heal')
    .then(updateGameState)
    .catch(console.error)
    .finally(enableButtons);
}

// --- Use Item Action ---
function useItem() {
  disableButtons();
  axios.post('/use-item')
    .then(updateGameState)
    .catch(console.error)
    .finally(enableButtons);
}

// --- Shared Update Handler ---
function updateGameState(response) {
  const data = response.data;

  // Update health bars
  document.getElementById("player-health").textContent =
    `${data.player_health} / ${data.player_max_health}`;
  document.getElementById("enemy-health").textContent =
    `${data.enemy_health} / ${data.enemy_max_health}`;

  // Add to combat log
  const logBox = document.getElementById("log-messages");
  const logMessage = data.message || "[No message]";
  logBox.textContent = logMessage + "\n" + logBox.textContent;
  logBox.scrollTop = 0;
}

// --- Button State Management ---
function disableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = true);
}

function enableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = false);
}
