import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security import create_access_token

client = TestClient(app)

@pytest.fixture
def auth_header():
    token = create_access_token(data={"sub": "admin"})
    return {"Authorization": f"Bearer {token}"}

def test_chat_qwen_missing_keys(auth_header):
    # Test Qwen model without keys should fallback to Local Mode message
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "model": "qwen"},
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "Local Mode" in data["response"]
    assert "QWEN" in data["response"]
