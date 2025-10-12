import os
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_database):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_ai_service():
    mock_generate = AsyncMock(return_value=[
        {"front": "Mock question 1", "back": "Correct answer 1"},
        {"front": "Mock question 2", "back": "Correct answer 2"}
    ])

    with patch('app.api.test_sets.generate_flashcards', mock_generate):
        yield mock_generate


@pytest.fixture
def test_set(client):
    response = client.post("/api/testset/", json={
        "title": "Test Set",
        "source_type": "text",
        "source_content": "Test content",
        "generation_params": {}
    })
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def test_card(client, test_set):
    response = client.post(
        f"/api/testset/{test_set['id']}/testcard/",
        json={"front_side": "Mock question 1", "back_side": "Correct answer 1", "position": 0}
    )
    assert response.status_code == 201
    return response.json()
