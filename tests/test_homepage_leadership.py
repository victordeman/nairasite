import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_homepage_leadership_info():
    """
    Test that the homepage renders and contains the updated leadership information for Prof. Ekpe Okorafor.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "PROF. Ekpe Okorafor" in response.text
    assert "B.Sc. Electronic Engr. (UNN)" in response.text
    assert "M.Sc. Comp. Eng. (Texas A&M)" in response.text
    assert "Ph.D. Comp. Eng. (Texas A&M)" in response.text
    assert "/static/images/prof-ekpe-okorafor.jpg" in response.text
