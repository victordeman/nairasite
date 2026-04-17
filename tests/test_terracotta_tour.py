
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_terracotta_tour_page_loads():
    response = client.get("/terracotta-tour")
    assert response.status_code == 200
    assert b"Terracotta 3D Tour" in response.content

def test_immersive_learning_page_contains_terracotta():
    response = client.get("/immersive-learning")
    assert response.status_code == 200
    assert b"Terracotta 3D Tour" in response.content
