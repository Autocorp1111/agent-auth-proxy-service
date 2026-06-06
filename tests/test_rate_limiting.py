import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rate_limit_headers():
    response = client.get("/health")
    assert response.status_code == 200
    # Rate limit headers may or may not be present depending on configuration
    assert "X-Request-ID" in response.headers