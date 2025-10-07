import pytest


@pytest.fixture
def test_set(client):
    response = client.post("/api/testset/", json={
        "title": "Test Set",
        "source_type": "text",
        "source_content": "Content",
        "generation_params": {}
    })
    return response.json()


@pytest.fixture
def test_card(client, test_set):
    response = client.post(
        f"/api/testset/{test_set['id']}/testcard/",
        json={"front_side": "Q", "back_side": "A", "position": 0}
    )
    return response.json()


def test_create_test_card(client, test_set):
    response = client.post(f"/api/testset/{test_set['id']}/testcard/", json={
        "front_side": "Question",
        "back_side": "Answer",
        "position": 0
    })
    assert response.status_code == 201
    assert response.json()["front_side"] == "Question"


def test_create_card_for_nonexistent_set(client):
    response = client.post("/api/testset/999/testcard/", json={
        "front_side": "Q", "back_side": "A", "position": 0
    })
    assert response.status_code == 404


def test_get_test_cards(client, test_set):
    set_id = test_set['id']
    client.post(
        f"/api/testset/{set_id}/testcard/",
        json={"front_side": "Q1", "back_side": "A1", "position": 0}
    )
    client.post(
        f"/api/testset/{set_id}/testcard/",
        json={"front_side": "Q2", "back_side": "A2", "position": 1}
    )

    response = client.get(f"/api/testset/{set_id}/testcard/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_test_card(client, test_card, test_set):
    response = client.get(f"/api/testset/{test_set['id']}/testcard/{test_card['id']}")
    assert response.status_code == 200
    assert response.json()["front_side"] == "Q"


def test_update_test_card(client, test_card, test_set):
    response = client.put(
        f"/api/testset/{test_set['id']}/testcard/{test_card['id']}",
        json={"front_side": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["front_side"] == "Updated"


def test_delete_test_card(client, test_card, test_set):
    set_id, card_id = test_set['id'], test_card['id']
    assert client.delete(f"/api/testset/{set_id}/testcard/{card_id}").status_code == 204
    assert client.get(f"/api/testset/{set_id}/testcard/{card_id}").status_code == 404


def test_word_count_validation(client, test_set):
    long_text = " ".join(["word"] * 51)
    response = client.post(f"/api/testset/{test_set['id']}/testcard/", json={
        "front_side": long_text, "back_side": "A", "position": 0
    })
    assert response.status_code == 422
    assert "Must be ≤50 words" in response.text
