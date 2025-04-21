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

function updateGameState(response) {
  const data = response.data;
  document.getElementById("player-health").textContent = `${data.player_health} / ${data.player_max_health}`;
  document.getElementById("enemy-health").textContent = `${data.enemy_health} / ${data.enemy_max_health}`;
  const logBox = document.getElementById("log-messages");
  logBox.textContent = (data.message || "[No message]") + "\n" + logBox.textContent;
  logBox.scrollTop = 0;
}

function disableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = true);
}
function enableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = false);
}
