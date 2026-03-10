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

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_cors_restricted():
    # Test with an unauthorized origin
    response = client.get("/healthz", headers={"Origin": "http://evil.com"})
    # CORSMiddleware doesn't necessarily block the request, it just doesn't add the CORS headers
    assert "access-control-allow-origin" not in response.headers

@pytest.mark.skipif(os.getenv("TESTING") == "1", reason="Rate limiting disabled in testing mode")
def test_rate_limiting_contact():
    # We should be able to hit the endpoint a few times, but it might fail because it's POST and requires body/auth
    # Actually /api/contact requires auth according to the router dependencies
    # Let's test /auth/token which is public but rate limited

    # Resetting limits between tests might be hard without more config,
    # but let's just try to hit it 6 times (limit is 5/minute)
    for i in range(5):
        response = client.post("/auth/token", data={"username": "test", "password": "test"})
        # We expect 401 because creds are wrong, but it shouldn't be 429 yet
        assert response.status_code == 401

    response = client.post("/auth/token", data={"username": "test", "password": "test"})
    assert response.status_code == 429
