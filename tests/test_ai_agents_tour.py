from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ai_agents_tour_page_loads():
    response = client.get("/ai-agents-tour")
    assert response.status_code == 200
    assert b"AI Agents 3D Tour" in response.content
    assert b"Autonomous Intelligence" in response.content

def test_immersive_learning_page_contains_ai_agents():
    response = client.get("/immersive-learning")
    assert response.status_code == 200
    assert b"/ai-agents-tour" in response.content
