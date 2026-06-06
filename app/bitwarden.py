"""
Bitwarden CLI Client for Agent Auth Proxy
This is the ONLY module allowed to call the bw CLI.
"""

import asyncio
import json
import os
import subprocess
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


class BitwardenError(Exception):
    """Base exception for all Bitwarden-related errors."""
    pass


class BitwardenUnavailableError(BitwardenError):
    """Bitwarden CLI or service is unavailable."""
    pass


class BitwardenAuthError(BitwardenError):
    """Authentication or session issues with Bitwarden."""
    pass


class BitwardenCLINotFoundError(BitwardenUnavailableError):
    """The 'bw' CLI binary is not installed or not in PATH."""
    pass


class BitwardenRateLimitError(BitwardenUnavailableError):
    """Bitwarden CLI rate limit or too many requests."""
    pass


class BitwardenClient:
    def __init__(self, email: str, master_password: str, collection_id: str):
        self.email = email
        self.master_password = master_password
        self.collection_id = collection_id
        self.session_token: Optional[str] = None
        self._lock = asyncio.Lock()
        self._max_retries = 3

    async def _run_bw(
        self, args: list[str], timeout: int = 30, extra_env: dict | None = None
    ) -> tuple[int, str, str]:
        """Run bw CLI as subprocess using thread executor to avoid blocking the event loop."""
        cmd = ["bw"] + args

        def _sync_run():
            env = {**os.environ, "PATH": os.environ.get("PATH", "")}
            if extra_env:
                env.update(extra_env)
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )
                return result.returncode, result.stdout.strip(), result.stderr.strip()
            except FileNotFoundError:
                return 127, "", "bw: command not found"
            except subprocess.TimeoutExpired:
                return 1, "", "Command timed out"
            except Exception as e:
                return 1, "", str(e)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _sync_run)

    def _sanitize_error(self, stderr: str, context: str = "") -> str:
        """Strip raw CLI output and return safe internal error message."""
        if not stderr:
            return f"bw_cli_error: {context or 'unknown'}"

        stderr_lower = stderr.lower()

        if "command not found" in stderr_lower or "bw: command not found" in stderr_lower:
            return "bw_cli_error: cli_not_found"
        if "session key is invalid" in stderr_lower or "invalid session" in stderr_lower:
            return "bw_cli_error: invalid_session"
        if "not found" in stderr_lower:
            return "bw_cli_error: item_not_found"
        if "unlock" in stderr_lower or "master password" in stderr_lower:
            return "bw_cli_error: unlock_failed"
        if "rate limit" in stderr_lower or "too many requests" in stderr_lower:
            return "bw_cli_error: rate_limited"
        if "network" in stderr_lower or "connection" in stderr_lower:
            return "bw_cli_error: network_error"

        return f"bw_cli_error: {context or 'generic_error'}"

    async def _ensure_session(self) -> str:
        """Ensure we have a valid session token. Only login if needed."""
        async with self._lock:
            if self.session_token:
                return self.session_token

            # bw status --raw always exits 0; parse JSON to detect auth state
            code, stdout, err = await self._run_bw(["status", "--raw"])
            if code != 0:
                safe_err = self._sanitize_error(err, "status")
                if "cli_not_found" in safe_err:
                    raise BitwardenCLINotFoundError(safe_err)
                raise BitwardenUnavailableError(safe_err)

            try:
                vault_status = json.loads(stdout).get("status", "unauthenticated")
            except (json.JSONDecodeError, AttributeError):
                vault_status = "unauthenticated"

            pw_env = {"BW_MASTER_PASSWORD": self.master_password}

            if vault_status == "unauthenticated":
                # Not logged in → login
                code, _, err = await self._run_bw(
                    ["login", self.email, "--passwordenv", "BW_MASTER_PASSWORD", "--raw"],
                    extra_env=pw_env,
                )
                if code != 0:
                    safe_err = self._sanitize_error(err, "login")
                    logger.error("bw_login_failed", error=safe_err)
                    if "cli_not_found" in safe_err:
                        raise BitwardenCLINotFoundError(safe_err)
                    raise BitwardenAuthError(safe_err)

            # Unlock (works even if already logged in)
            code, session, err = await self._run_bw(
                ["unlock", "--passwordenv", "BW_MASTER_PASSWORD", "--raw"],
                extra_env=pw_env,
            )
            if code != 0:
                safe_err = self._sanitize_error(err, "unlock")
                logger.error("bw_unlock_failed", error=safe_err)
                if "cli_not_found" in safe_err:
                    raise BitwardenCLINotFoundError(safe_err)
                raise BitwardenAuthError(safe_err)

            self.session_token = session
            logger.info("bw_session_established")
            return self.session_token

    async def get_credential(self, item_name: str) -> str:
        """Fetch credential value from Bitwarden (respecting collection)."""
        for attempt in range(self._max_retries):
            try:
                session = await self._ensure_session()

                # Use collection filter for security
                code, stdout, stderr = await self._run_bw([
                    "list", "items",
                    "--collectionid", self.collection_id,
                    "--search", item_name,
                    "--session", session,
                    "--raw"
                ])

                if code == 0:
                    try:
                        items = json.loads(stdout)
                        if not items:
                            raise BitwardenUnavailableError("bw_cli_error: item_not_found")

                        # Take first match
                        item = items[0]
                        password = item.get("login", {}).get("password") or item.get("password")
                        if not password:
                            raise BitwardenUnavailableError("bw_cli_error: no_password_field")
                        return password
                    except json.JSONDecodeError:
                        raise BitwardenUnavailableError("bw_cli_error: invalid_json_response")

                # Handle session expiry
                if "invalid" in stderr.lower() or "expired" in stderr.lower():
                    logger.warning("bw_session_expired", attempt=attempt + 1)
                    self.session_token = None
                    continue

                safe_err = self._sanitize_error(stderr, f"get_item:{item_name}")

                if "cli_not_found" in safe_err:
                    raise BitwardenCLINotFoundError(safe_err)
                if "rate_limited" in safe_err:
                    raise BitwardenRateLimitError(safe_err)
                if "invalid_session" in safe_err or "unlock_failed" in safe_err:
                    raise BitwardenAuthError(safe_err)

                raise BitwardenUnavailableError(safe_err)

            except (BitwardenUnavailableError, BitwardenAuthError, BitwardenCLINotFoundError, BitwardenRateLimitError):
                # Do not retry genuine Bitwarden errors
                raise
            except Exception as e:
                if attempt == self._max_retries - 1:
                    raise BitwardenUnavailableError(f"bw_cli_error: unexpected_error:{str(e)}")
                await asyncio.sleep(1 * (attempt + 1))  # exponential backoff

        raise BitwardenUnavailableError(f"bw_cli_error: max_retries_exceeded:{item_name}")

    async def ping(self) -> bool:
        """Lightweight connectivity check: runs 'bw status' to verify the CLI is reachable."""
        code, stdout, _ = await self._run_bw(["status", "--raw"], timeout=10)
        if code != 0:
            return False
        try:
            status = json.loads(stdout)
            return isinstance(status, dict) and "status" in status
        except (json.JSONDecodeError, TypeError):
            return False