let cards = [];
let currentIndex = 0;
const setId = localStorage.getItem("currentSetId");

async function loadTest() {
  if (!setId) {
    alert("No test set selected");
    window.location.href = "/";
    return;
  }

  cards = await api.getTestCards(setId);
  const savedIndex = localStorage.getItem("currentCardIndex");
  if (savedIndex) {
    currentIndex = parseInt(savedIndex);
    localStorage.removeItem("currentCardIndex");
  }

  renderTest();
}

function renderTest() {
  const card = cards[currentIndex];
  document.getElementById("card-front").textContent = card.front_side;
  document.getElementById("answer-input").value = "";
  document.getElementById("result").className = "result hidden";

  document.getElementById("prev-btn").disabled = currentIndex === 0;
  document.getElementById("next-btn").disabled =
    currentIndex === cards.length - 1;
}

async function submitAnswer() {
  const answer = document.getElementById("answer-input").value.trim();
  if (!answer) return;

  const card = cards[currentIndex];
  const result = await api.submitScore(setId, card.id, answer);

  const resultDiv = document.getElementById("result");
  resultDiv.className = `result ${result.correct ? "correct" : "incorrect"}`;
  resultDiv.innerHTML = `
    <div>Score: ${(result.score * 100).toFixed(0)}%</div>
    <div>Expected: ${result.expected}</div>
  `;
}

function previousCard() {
  if (currentIndex > 0) {
    currentIndex--;
    renderTest();
  }
}

function nextCard() {
  if (currentIndex < cards.length - 1) {
    currentIndex++;
    renderTest();
  }
}

function exitTest() {
  window.location.href = "./test-cards.html";
}

loadTest();
