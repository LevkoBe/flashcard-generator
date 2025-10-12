def test_mock_is_applied(client, mock_ai_service):
    response = client.post("/api/testset/", json={
        "title": "Mock Test",
        "source_type": "text",
        "source_content": "Some text",
        "generation_params": {}
    })

    assert response.status_code == 201
    assert mock_ai_service.called
    assert mock_ai_service.call_count == 1

    data = response.json()
    assert len(data["cards"]) == 2
    assert data["cards"][0]["front_side"] == "Mock question 1"
