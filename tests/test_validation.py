
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database import init_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    import asyncio
    asyncio.run(init_db())

client = TestClient(app)

def test_captcha_generation():
    response = client.get("/api/captcha")
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "captcha_token" in data

def test_contact_validation_fail_no_captcha():
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello world this is a long enough message"
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "CAPTCHA required"

def test_contact_honeypot():
    # Bots filling honeypot should get a success but it's not really saved
    payload = {
        "name": "Bot",
        "email": "bot@example.com",
        "message": "I am a bot spamming you",
        "website_url": "http://spam.com"
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 201
    assert response.json()["success"] is True

def test_newsletter_honeypot():
    payload = {
        "email": "bot@example.com",
        "website_url": "http://spam.com"
    }
    response = client.post("/api/newsletter", json=payload)
    assert response.status_code == 201
    assert response.json()["success"] is True

def test_contact_wrong_captcha():
    captcha_res = client.get("/api/captcha")
    token = captcha_res.json()["captcha_token"]

    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello world this is a long enough message",
        "captcha_token": token,
        "captcha_answer": "999" # definitely wrong
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect CAPTCHA answer"

def test_contact_success():
    # This is tricky because I need the answer from the token.
    # Since I'm using JWT and I know the secret (or I can mock it)
    # Actually, for the test I can just use a real one if I can "calculate" the answer.
    # But the question is a string like "5 + 3 = ?"

    captcha_res = client.get("/api/captcha")
    data = captcha_res.json()
    question = data["question"]
    token = data["captcha_token"]

    # Parse question "a + b = ?"
    parts = question.split(" ")
    ans = str(int(parts[0]) + int(parts[2]))

    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello world this is a long enough message",
        "captcha_token": token,
        "captcha_answer": ans
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 201
    assert response.json()["success"] is True
