// --- Demo Button: Click Counter ---
const button = document.getElementById('myButton');
const clickCount = document.getElementById('clickCount');

if (button && clickCount) {
  button.addEventListener('click', function () {
    axios.post('/increment')
      .then(function (response) {
        clickCount.textContent = response.data.count;
      })
      .catch(function (error) {
        console.log(error);
      });
  });
}

// --- Demo Input: Flip Case ---
const inputText = document.getElementById('inputText');
const flipButton = document.getElementById('flipButton');
const result = document.getElementById('result');

if (flipButton && inputText && result) {
  flipButton.addEventListener('click', function () {
    const text = inputText.value;
    axios.post('/flip_case', { text: text })
      .then(function (response) {
        result.textContent = response.data.flipped_text;
      })
      .catch(function (error) {
        console.log(error);
      });
  });
}

// --- Game Ability Attack ---
function useAbility(abilityName) {
  axios.post('/attack', { ability: abilityName })
    .then(function (response) {
      const data = response.data;

      // Update health displays
      document.getElementById("player-health").textContent =
        `${data.player_health} / ${data.player_max_health}`;
      document.getElementById("enemy-health").textContent =
        `${data.enemy_health} / ${data.enemy_max_health}`;

      // Update combat log with both player + enemy messages
      const logBox = document.getElementById("log-messages");
      const logMessage = `${data.message}\n${data.enemy_message}`;
      logBox.textContent = logMessage + "\n\n" + logBox.textContent;

      // Optional: Auto-scroll log to top
      logBox.scrollTop = 0;
    })
    .catch(function (error) {
      console.error("Attack failed:", error);
    });
}
