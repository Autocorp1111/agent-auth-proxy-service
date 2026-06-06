"""Tests for health endpoints"""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.main import app
from app.routes.health import readiness_probe


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class FakeDB:
    async def execute(self, statement):
        assert str(statement) == str(text("SELECT 1"))


class FakeBitwarden:
    async def ping(self):
        return True


@pytest.mark.asyncio
async def test_ready_endpoint_structure():
    response = await readiness_probe(
        request=None,
        db=FakeDB(),
        bitwarden=FakeBitwarden(),
    )

    assert response["status"] == "ready"
    assert response["checks"] == {"database": True, "bitwarden": True}