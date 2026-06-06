import pytest
import uuid
import secrets
from fastapi import HTTPException

from app.routes.agents import (
    register_agent,
    grant_credential_access,
    revoke_credential_access,
    RegisterAgentRequest,
)
from app.auth import hash_api_key, KEY_PREFIX_LEN
from app.database import Agent


async def _insert_agent(name: str, db) -> Agent:
    """Insert a bare agent row and return it (bypasses the register route)."""
    api_key = secrets.token_urlsafe(32)
    agent = Agent(
        name=name,
        api_key_hash=hash_api_key(api_key),
        key_prefix=api_key[:KEY_PREFIX_LEN],
    )
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


# --- register_agent ---

@pytest.mark.asyncio
async def test_register_agent_success(test_db):
    result = await register_agent(
        payload=RegisterAgentRequest(name="brand-new-agent"),
        admin=None,
        db=test_db,
    )
    assert result["name"] == "brand-new-agent"
    assert "api_key" in result
    assert "id" in result


@pytest.mark.asyncio
async def test_register_agent_duplicate_returns_409(test_db):
    await register_agent(
        payload=RegisterAgentRequest(name="dup-agent"),
        admin=None,
        db=test_db,
    )

    with pytest.raises(HTTPException) as exc_info:
        await register_agent(
            payload=RegisterAgentRequest(name="dup-agent"),
            admin=None,
            db=test_db,
        )

    assert exc_info.value.status_code == 409
    assert "already exists" in exc_info.value.detail


# --- grant_credential_access ---

@pytest.mark.asyncio
async def test_grant_access_nonexistent_agent_returns_404(test_db):
    with pytest.raises(HTTPException) as exc_info:
        await grant_credential_access(
            agent_id=uuid.uuid4(),
            credential_name="some-credential",
            admin=None,
            db=test_db,
        )
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_grant_access_duplicate_returns_409(test_db):
    agent = await _insert_agent("grant-agent", test_db)

    await grant_credential_access(
        agent_id=agent.id,
        credential_name="my-secret",
        admin=None,
        db=test_db,
    )

    with pytest.raises(HTTPException) as exc_info:
        await grant_credential_access(
            agent_id=agent.id,
            credential_name="my-secret",
            admin=None,
            db=test_db,
        )
    assert exc_info.value.status_code == 409


# --- revoke_credential_access ---

@pytest.mark.asyncio
async def test_revoke_access_nonexistent_agent_returns_404(test_db):
    with pytest.raises(HTTPException) as exc_info:
        await revoke_credential_access(
            agent_id=uuid.uuid4(),
            credential_name="some-credential",
            admin=None,
            db=test_db,
        )
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_revoke_access_no_grant_returns_404(test_db):
    agent = await _insert_agent("revoke-agent", test_db)

    with pytest.raises(HTTPException) as exc_info:
        await revoke_credential_access(
            agent_id=agent.id,
            credential_name="never-granted",
            admin=None,
            db=test_db,
        )
    assert exc_info.value.status_code == 404
