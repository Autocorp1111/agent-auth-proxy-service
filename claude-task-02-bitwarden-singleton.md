# Claude Task: Bitwarden Client Singleton

**Project:** /mnt/e/Agents/project/agent-auth-proxy
**Scope:** Single focused improvement

**Task:**
Convert the Bitwarden client so it is instantiated once and stored in `app.state` (using FastAPI lifespan) instead of being created on every request.

**Requirements:**
- Use FastAPI's lifespan context manager
- Store the Bitwarden client in `app.state.bitwarden`
- Update dependencies so routes use the singleton from app.state
- Make minimal, clean changes
- Do not change business logic, only instantiation pattern

Focus only on this change.