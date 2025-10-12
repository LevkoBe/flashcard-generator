def test_create_test_set(client):
    response = client.post("/api/testset/", json={
        "title": "New Set",
        "source_type": "text",
        "source_content": "Text",
        "generation_params": {}
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Set"
    assert len(data["cards"]) == 2


def test_get_test_sets(client):
    client.post(
        "/api/testset/",
        json={"title": "s1", "source_type": "text", "source_content": "T", "generation_params": {}}
    )
    client.post(
        "/api/testset/",
        json={"title": "s2", "source_type": "text", "source_content": "T", "generation_params": {}}
    )

    response = client.get("/api/testset/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_test_set(client, test_set):
    response = client.get(f"/api/testset/{test_set['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Set"


def test_get_test_set_not_found(client):
    assert client.get("/api/testset/999").status_code == 404


def test_update_test_set(client, test_set):
    response = client.put(f"/api/testset/{test_set['id']}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_test_set(client, test_set):
    test_id = test_set['id']
    assert client.delete(f"/api/testset/{test_id}").status_code == 204
    assert client.get(f"/api/testset/{test_id}").status_code == 404
