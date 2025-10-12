let cards = [];
let activeCardId = null;
let flippedCards = new Set();
const setId = localStorage.getItem("currentSetId");

async function loadCards() {
  if (!setId) {
    alert("No test set selected");
    window.location.href = "/";
    return;
  }
  cards = await api.getTestCards(setId);
  renderCards();
}

function renderCards() {
  const grid = document.getElementById("cards-grid");
  grid.innerHTML = cards
    .map((card) => {
      const isFlipped = flippedCards.has(card.id);
      const text = isFlipped ? card.back_side : card.front_side;
      return `
      <div class="card ${card.id === activeCardId ? "active" : ""} 
                        ${isFlipped ? "flipped" : ""}"
           onclick="selectCard(${card.id})"
           ondblclick="toggleFlip(${card.id})">
        ${text.substring(0, 100)}${text.length > 100 ? "..." : ""}
      </div>
    `;
    })
    .join("");
}

function selectCard(id) {
  activeCardId = id;
  renderCards();
}

function toggleFlip(id) {
  if (flippedCards.has(id)) {
    flippedCards.delete(id);
  } else {
    flippedCards.add(id);
  }
  renderCards();
}

async function createCard() {
  const front = prompt("Front side (question):");
  if (!front) return;
  const back = prompt("Back side (answer):");
  if (!back) return;

  await api.createTestCard(setId, {
    front_side: front,
    back_side: back,
    position: cards.length,
  });

  await loadCards();
}

async function deleteCard() {
  if (!activeCardId || !confirm("Delete this card?")) return;
  await api.deleteTestCard(setId, activeCardId);
  activeCardId = null;
  await loadCards();
}

function editCard() {
  alert("Edit not implemented (use delete + create)");
}

function testCard() {
  if (!activeCardId) return;
  localStorage.setItem(
    "currentCardIndex",
    cards.findIndex((c) => c.id === activeCardId)
  );
  window.location.href = "./card-test.html";
}

function goBack() {
  window.location.href = "/";
}

loadCards();
