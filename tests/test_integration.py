import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Test that endpoints require authentication"""
    response = await client.get("/credentials/google_oauth")
    assert response.status_code in (401, 403)

# More tests for credential flow, registration, and access management
# would be added once a test database and mocked Bitwarden are set up.