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
        "user_answer": "Nearly correct answer",
    })
    assert response.status_code == 201
    assert response.json()["correct"] is True


def test_create_faulty_score(client, test_set, test_card):
    response = client.post(f"/api/testset/{test_set['id']}/testcard/{test_card['id']}/score", json={
        "user_answer": "Incorrect and far from close",
    })
    assert response.status_code == 201
    assert response.json()["correct"] is False
