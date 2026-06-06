You are fixing the P0 issues identified in the final review of the Agent Auth Proxy.

**Project:** /mnt/e/Agents/project/agent-auth-proxy

**P0 Issues to Fix:**

1. Fix `ImportError`: Move `hash_api_key` import from `agents.py` to come from `app.auth`
2. Enforce access control in `credentials.py` — check the `CredentialAccess` table before returning a credential
3. Create proper Alembic migrations (initial migration for all tables)
4. Fix rate limiting by adding `request: Request` parameter to rate-limited endpoints

Fix these issues one by one and verify the code is correct after each fix.