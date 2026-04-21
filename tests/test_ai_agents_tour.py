import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ai_agents_tour_route():
    response = client.get("/ai-agents-tour")
    assert response.status_code == 200
    assert "AI Agents 3D Tour" in response.text
    assert "Autonomous Intelligence" in response.text
    assert "Alan Turing" in response.text
    assert "ReAct Framework" in response.text

def test_homepage_integration():
    response = client.get("/")
    assert response.status_code == 200
    assert "Enter AI Agents Tour" in response.text
    assert "launch-ai-tour" in response.text

def test_immersive_learning_integration():
    response = client.get("/immersive-learning")
    assert response.status_code == 200
    assert "AI Agents 3D Tour" in response.text
    assert "/ai-agents-tour" in response.text
