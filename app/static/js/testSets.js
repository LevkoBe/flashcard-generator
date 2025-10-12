let testSets = [];
let activeSetId = null;

async function loadTestSets() {
  testSets = await api.getTestSets();
  renderTestSets();
}

function renderTestSets() {
  const grid = document.getElementById("test-sets-grid");
  grid.innerHTML = testSets
    .map(
      (set) => `
    <div class="item ${set.id === activeSetId ? "active" : ""}" 
         onclick="selectTestSet(${set.id})"
         ondblclick="openTestCards(${set.id})">
      <strong>${set.title}</strong>
      <small style="color: var(--text-secondary)">
        ${set.cards?.length || 0} cards
      </small>
    </div>
  `
    )
    .join("");
}

function selectTestSet(id) {
  activeSetId = id;
  renderTestSets();
}

function openTestCards(id) {
  localStorage.setItem("currentSetId", id);
  window.location.href = "./test-cards.html";
}

async function createTestSet() {
  const url = prompt("Enter URL or paste text:");
  if (!url) return;

  const isUrl = url.startsWith("http");
  const quantity = prompt("Number of cards (leave empty for auto):", "");

  await api.createTestSet({
    title: isUrl ? new URL(url).hostname : "Custom Text",
    source_type: isUrl ? "url" : "text",
    source_content: url,
    generation_params: quantity ? { quantity: parseInt(quantity) } : {},
  });

  await loadTestSets();
}

async function deleteTestSet() {
  if (!activeSetId || !confirm("Delete this test set?")) return;
  await api.deleteTestSet(activeSetId);
  activeSetId = null;
  await loadTestSets();
}

function editTestSet() {
  if (!activeSetId) return;
  openTestCards(activeSetId);
}

function testTestSet() {
  if (!activeSetId) return;
  localStorage.setItem("currentSetId", activeSetId);
  window.location.href = "./card-test.html";
}

loadTestSets();
