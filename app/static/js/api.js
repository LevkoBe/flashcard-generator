const API_BASE = "http://localhost:8000/api";

const api = {
  async getTestSets() {
    const res = await fetch(`${API_BASE}/testset/`);
    return res.json();
  },

  async createTestSet(data) {
    const res = await fetch(`${API_BASE}/testset/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async deleteTestSet(id) {
    await fetch(`${API_BASE}/testset/${id}`, { method: "DELETE" });
  },

  async getTestCards(setId) {
    const res = await fetch(`${API_BASE}/testset/${setId}/testcard/`);
    return res.json();
  },

  async createTestCard(setId, data) {
    const res = await fetch(`${API_BASE}/testset/${setId}/testcard/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async deleteTestCard(setId, cardId) {
    await fetch(`${API_BASE}/testset/${setId}/testcard/${cardId}`, {
      method: "DELETE",
    });
  },

  async submitScore(setId, cardId, answer) {
    const res = await fetch(
      `${API_BASE}/testset/${setId}/testcard/${cardId}/score`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_answer: answer }),
      }
    );
    return res.json();
  },
};
