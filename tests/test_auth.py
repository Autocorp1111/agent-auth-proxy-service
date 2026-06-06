import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock
from fastapi.security import HTTPAuthorizationCredentials
import bcrypt

from app.auth import hash_api_key, get_current_agent
from app.database import Agent


def test_hash_api_key():
    key = "test-api-key-123"
    hashed = hash_api_key(key)
    assert hashed != key
    assert len(hashed) > 50


# --- Finding 2: last_seen_at must be persisted after successful authentication ---


@pytest.mark.asyncio
async def test_last_seen_at_persisted_after_auth(test_db):
    """get_current_agent must commit last_seen_at so it survives beyond the call."""
    api_key = "testkey1234567890abcdefghijklmno"  # 32 chars
    key_hash = bcrypt.hashpw(api_key.encode(), bcrypt.gensalt()).decode()
    old_time = datetime.now(timezone.utc) - timedelta(hours=2)

    agent = Agent(
        name="auth-test-agent",
        api_key_hash=key_hash,
        key_prefix=api_key[:8],
        last_seen_at=old_time,
    )
    test_db.add(agent)
    await test_db.commit()
    # Refresh so original_last_seen is the naive datetime SQLite actually stored,
    # matching the naive value that will come back after the second refresh below.
    await test_db.refresh(agent)
    original_last_seen = agent.last_seen_at

    request = MagicMock()
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=api_key)

    returned_agent = await get_current_agent(
        request=request, credentials=credentials, db=test_db
    )

    # Refresh from DB to confirm the commit actually wrote to storage
    await test_db.refresh(returned_agent)

    assert returned_agent.last_seen_at is not None
    assert returned_agent.last_seen_at > original_last_seen, (
        "last_seen_at was not updated and persisted by get_current_agent"
    )