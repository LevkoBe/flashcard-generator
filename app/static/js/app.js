let state = {
  view: "sets",
  sets: [],
  currentSet: null,
  currentCard: null,
  selectedSetId: null,
  selectedCardId: null,
};

async function init() {
  await loadTestSets();
  render();
  setupEventListeners();
}

async function loadTestSets() {
  state.sets = await api.getTestSets();
}

function render() {
  const app = document.getElementById("app");

  if (state.view === "sets") {
    app.innerHTML = renderSetsView();
  } else if (state.view === "cards") {
    app.innerHTML = renderCardsView();
  } else if (state.view === "test") {
    app.innerHTML = renderTestView();
  }
}

function renderSetsView() {
  return `
    <div class="container">
      <h1>Test Sets</h1>
      <button class="btn" onclick="openUploadModal()">+ Create Test Set</button>
      <div class="grid">
        ${state.sets
          .map(
            (set) => `
          <div class="card ${state.selectedSetId === set.id ? "selected" : ""}" 
               onclick="selectSet(${set.id})"
               ondblclick="viewCards(${set.id})">
            <h3>${set.title}</h3>
            <p>${set.cards.length} cards</p>
            <p>Avg: ${
              set.average_score ? set.average_score.toFixed(2) : "N/A"
            }</p>
          </div>
        `
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderCardsView() {
  return `
    <div class="container">
      <button class="btn back-btn" onclick="backToSets()">← Back</button>
      <h1>${state.currentSet.title}</h1>
      <div class="grid">
        ${state.currentSet.cards
          .map(
            (card) => `
          <div class="card ${
            state.selectedCardId === card.id ? "selected" : ""
          }"
               onclick="selectCard(${card.id})"
               ondblclick="testCard(${card.id})">
            <h3>Card #${card.position + 1}</h3>
            <p>${card.front_side.substring(0, 50)}...</p>
            <p>Avg: ${
              card.average_score ? card.average_score.toFixed(2) : "N/A"
            }</p>
          </div>
        `
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderTestView() {
  const card = state.currentCard;
  return `
    <div class="container">
      <button class="btn back-btn" onclick="backToCards()">← Back</button>
      <h1>Test Card #${card.position + 1}</h1>
      <div class="flashcard" id="flashcard" ondblclick="flipCard()">
        <p id="card-content">${card.front_side}</p>
      </div>
      <div class="answer-input">
        <input type="text" id="answer" placeholder="Type your answer here..." />
        <button class="btn" onclick="submitAnswer()">Submit</button>
      </div>
      <div id="feedback"></div>
    </div>
  `;
}

function selectSet(id) {
  state.selectedSetId = id;
  render();
}

async function viewCards(id) {
  state.currentSet = await api.getTestSet(id);
  state.view = "cards";
  state.selectedCardId = null;
  render();
}

function selectCard(id) {
  state.selectedCardId = id;
  render();
}

function testCard(id) {
  state.currentCard = state.currentSet.cards.find((c) => c.id === id);
  state.view = "test";
  render();
}

function flipCard() {
  const flashcard = document.getElementById("flashcard");
  const content = document.getElementById("card-content");

  flashcard.classList.toggle("flipped");
  content.textContent = flashcard.classList.contains("flipped")
    ? state.currentCard.back_side
    : state.currentCard.front_side;
}

async function submitAnswer() {
  const answer = document.getElementById("answer").value;
  const result = await api.submitScore(
    state.currentSet.id,
    state.currentCard.id,
    answer
  );

  const feedback = document.getElementById("feedback");
  feedback.className = `feedback ${result.correct ? "correct" : "incorrect"}`;
  feedback.innerHTML = `
    <p>Score: ${(result.score * 100).toFixed(0)}%</p>
    <p>${result.correct ? "✓ Correct!" : "✗ Incorrect"}</p>
    <p>Expected: ${result.expected}</p>
  `;
}

function backToSets() {
  state.view = "sets";
  state.currentSet = null;
  loadTestSets().then(render);
}

function backToCards() {
  state.view = "cards";
  state.currentCard = null;
  render();
}

function openUploadModal() {
  document.getElementById("uploadModal").classList.add("active");
}

function closeUploadModal() {
  document.getElementById("uploadModal").classList.remove("active");
}

async function handleUpload(e) {
  e.preventDefault();
  const formData = {
    title: document.getElementById("title").value,
    source_type: document.getElementById("sourceType").value,
    source_content: document.getElementById("sourceContent").value,
    generation_params: {
      guidance: document.getElementById("guidance").value || undefined,
      quantity:
        parseInt(document.getElementById("quantity").value) || undefined,
    },
  };

  await api.createTestSet(formData);
  closeUploadModal();
  await loadTestSets();
  render();
}

function setupEventListeners() {
  document
    .getElementById("uploadForm")
    .addEventListener("submit", handleUpload);
  document.getElementById("uploadModal").addEventListener("click", (e) => {
    if (e.target.id === "uploadModal") closeUploadModal();
  });
}

init();
