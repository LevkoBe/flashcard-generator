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
        json={"front_side": "What do I say?", "back_side": "Correct answer", "position": 0}
    )
    return response.json()


def test_create_perfect_score(client, test_set, test_card):
    response = client.post(f"/api/testset/{test_set['id']}/testcard/{test_card['id']}/score", json={
        "user_answer": "Correct answer",
    })
    assert response.status_code == 201
    assert response.json()["correct"] is True


def test_create_score_for_nonexistent_set(client):
    response = client.post("/api/testset/999/testcard/999/score", json={
        "user_answer": "Correct answer",
    })
    assert response.status_code == 404


def test_create_imperfect_score(client, test_set, test_card):
    response = client.post(f"/api/testset/{test_set['id']}/testcard/{test_card['id']}/score", json={
        "user_answer": "Imperfect answer",
    })
    assert response.status_code == 201
    assert response.json()["correct"] is True


def test_create_faulty_score(client, test_set, test_card):
    response = client.post(f"/api/testset/{test_set['id']}/testcard/{test_card['id']}/score", json={
        "user_answer": "Incorrect and far from close",
    })
    assert response.status_code == 201
    assert response.json()["correct"] is False
