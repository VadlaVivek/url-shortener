# tests/test_basic.py
import pytest
from app.main import app, store

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_shorten_url(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 201
    assert "short_code" in res.json

def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "not_a_url"})
    assert res.status_code == 400

def test_redirect(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = res.json["short_code"]
    redir = client.get(f"/{short_code}", follow_redirects=False)
    assert redir.status_code == 302

def test_stats(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = res.json["short_code"]
    client.get(f"/{short_code}")
    stats = client.get(f"/api/stats/{short_code}")
    assert stats.status_code == 200
    assert stats.json["clicks"] == 1
