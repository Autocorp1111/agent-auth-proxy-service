"""Unit tests for BitwardenClient"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.bitwarden import (
    BitwardenClient,
    BitwardenUnavailableError,
    BitwardenCLINotFoundError,
)


@pytest.fixture
def client():
    return BitwardenClient(
        email="test@example.com",
        master_password="testpass",
        collection_id="test-collection"
    )


@pytest.mark.asyncio
async def test_ping_success(client):
    """Test successful ping"""
    with patch.object(client, "_run_bw", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = (0, '{"status": "unlocked"}', "")
        result = await client.ping()
        assert result is True


@pytest.mark.asyncio
async def test_ping_failure(client):
    """Test failed ping"""
    with patch.object(client, "_run_bw", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = (1, "", "error")
        result = await client.ping()
        assert result is False


@pytest.mark.asyncio
async def test_cli_not_found(client):
    """Test CLI not found error"""
    with patch.object(client, "_run_bw", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = (127, "", "bw: command not found")
        with pytest.raises(BitwardenCLINotFoundError):
            await client.get_credential("test-item")


# --- Finding 1: BW_MASTER_PASSWORD must be injected into subprocess env ---


@pytest.mark.asyncio
async def test_run_bw_passes_extra_env_to_subprocess(client):
    """_run_bw must merge extra_env into the subprocess environment."""
    captured_env = {}

    def fake_subprocess_run(cmd, **kwargs):
        captured_env.update(kwargs.get("env", {}))
        m = MagicMock()
        m.returncode = 0
        m.stdout = ""
        m.stderr = ""
        return m

    with patch("app.bitwarden.subprocess.run", side_effect=fake_subprocess_run):
        await client._run_bw(["status"], extra_env={"BW_MASTER_PASSWORD": "secret123"})

    assert captured_env.get("BW_MASTER_PASSWORD") == "secret123"


@pytest.mark.asyncio
async def test_ensure_session_passes_master_password_to_login_and_unlock(client):
    """_ensure_session must supply BW_MASTER_PASSWORD in extra_env for login and unlock."""
    run_calls = []

    async def capturing_run_bw(args, timeout=30, extra_env=None):
        run_calls.append({"args": list(args), "extra_env": dict(extra_env) if extra_env else None})
        if args[0] == "status":
            return 0, '{"status": "unauthenticated"}', ""
        if args[0] == "login":
            return 0, "", ""
        if args[0] == "unlock":
            return 0, "fake-session-token", ""
        return 0, "", ""

    with patch.object(client, "_run_bw", side_effect=capturing_run_bw):
        client.session_token = None
        await client._ensure_session()

    login_call = next(c for c in run_calls if c["args"][0] == "login")
    unlock_call = next(c for c in run_calls if c["args"][0] == "unlock")

    assert login_call["extra_env"] is not None, "login must receive extra_env"
    assert login_call["extra_env"].get("BW_MASTER_PASSWORD") == client.master_password

    assert unlock_call["extra_env"] is not None, "unlock must receive extra_env"
    assert unlock_call["extra_env"].get("BW_MASTER_PASSWORD") == client.master_password


@pytest.mark.asyncio
async def test_master_password_not_in_subprocess_args(client):
    """Master password must not appear as a CLI argument — only via env."""
    captured_cmds = []

    def fake_subprocess_run(cmd, **kwargs):
        captured_cmds.append(list(cmd))
        m = MagicMock()
        m.returncode = 0
        m.stdout = '{"status": "unauthenticated"}' if cmd[1] == "status" else "fake-session"
        m.stderr = ""
        return m

    with patch("app.bitwarden.subprocess.run", side_effect=fake_subprocess_run):
        client.session_token = None
        await client._ensure_session()

    for cmd in captured_cmds:
        assert client.master_password not in cmd, (
            f"master_password leaked into CLI args: {cmd}"
        )