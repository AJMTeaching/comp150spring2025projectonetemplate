// --- Click Counter Demo ---
const button = document.getElementById('myButton');
const clickCount = document.getElementById('clickCount');

if (button && clickCount) {
  button.addEventListener('click', function () {
    axios.post('/increment')
      .then(response => {
        clickCount.textContent = response.data.count;
      })
      .catch(console.log);
  });
}

// --- Flip Case Demo ---
const inputText = document.getElementById('inputText');
const flipButton = document.getElementById('flipButton');
const result = document.getElementById('result');

if (flipButton && inputText && result) {
  flipButton.addEventListener('click', function () {
    const text = inputText.value;
    axios.post('/flip_case', { text: text })
      .then(response => {
        result.textContent = response.data.flipped_text;
      })
      .catch(console.log);
  });
}

// --- Game Ability Attack ---
function useAbility(abilityName) {
  disableButtons();
  axios.post('/attack', { ability: abilityName })
    .then(updateGameState)
    .catch(error => console.error("Attack failed:", error))
    .finally(enableButtons);
}

// --- Heal Route ---
function heal() {
  disableButtons();
  axios.post('/heal')
    .then(updateGameState)
    .catch(error => console.error("Heal failed:", error))
    .finally(enableButtons);
}

// --- Use Item Route ---
function useItem() {
  disableButtons();
  axios.post('/use-item')
    .then(updateGameState)
    .catch(error => console.error("Item use failed:", error))
    .finally(enableButtons);
}

// --- Shared Update Handler ---
function updateGameState(response) {
  const data = response.data;

  // Update health displays
  document.getElementById("player-health").textContent =
    `${data.player_health} / ${data.player_max_health}`;
  document.getElementById("enemy-health").textContent =
    `${data.enemy_health} / ${data.enemy_max_health}`;

  // Update combat log
  const logBox = document.getElementById("log-messages");
  const logMessage = data.message || "[No message]";
  logBox.textContent = logMessage + "\n" + logBox.textContent;

  logBox.scrollTop = 0;
}

// --- Disable/Enable Buttons During Actions ---
function disableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = true);
}
function enableButtons() {
  document.querySelectorAll("button").forEach(btn => btn.disabled = false);
}
