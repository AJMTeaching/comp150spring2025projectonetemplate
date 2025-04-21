// --- Game Ability Attack ---
function useAbility(abilityName) {
  disableButtons();
  axios.post('/attack', { ability: abilityName })
    .then(response => {
      const data = response.data;
      if (data.redirect) {
        window.location.href = data.redirect;
      } else {
        updateGameState(data);
      }
    })
    .catch(console.error)
    .finally(enableButtons);
}

// --- Heal Action ---
function heal() {
  disableButtons();
  axios.post('/heal')
    .then(response => updateGameState(response.data))
    .catch(console.error)
    .finally(enableButtons);
}

// --- Use Item Action ---
function useItem() {
  disableButtons();
  axios.post('/use-item')
    .then(response => updateGameState(response.data))
    .catch(console.error)
    .finally(enableButtons);
}

// --- Shared Update Handler ---
function updateGameState(data) {
  document.getElementById("player-health").textContent =
    `${data.player_health} / ${data.player_max_health}`;
  document.getElementById("enemy-health").textContent =
    `${data.enemy_health} / ${data.enemy_max_health}`;

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
