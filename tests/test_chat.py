import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security import create_access_token

client = TestClient(app)

@pytest.fixture
def auth_header():
    token = create_access_token(data={"sub": "admin"})
    return {"Authorization": f"Bearer {token}"}

def test_chat_local_mode(auth_header):
    # Test with default local model (RAG fallback)
    response = client.post(
        "/api/chat",
        json={"message": "What are the strategic pillars?", "model": "local"},
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Strategic Pillar" in data["response"] or "pillars" in data["response"].lower()

def test_chat_missing_keys(auth_header):
    # Test premium models without keys should fallback to Local Mode message
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "model": "gemini"},
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "Local Mode" in data["response"]

def test_chat_requires_auth():
    # Chat should require a token again
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "model": "local"}
    )
    assert response.status_code == 401
