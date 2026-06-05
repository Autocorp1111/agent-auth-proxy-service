# Claude Task: Apply Rate Limiting

**Project:** /mnt/e/Agents/project/agent-auth-proxy
**Scope:** Single focused improvement

**Task:**
Apply the existing `limiter` (from slowapi) to the credential routes using `@limiter.limit()` decorators.

**Requirements:**
- Use the already configured `Limiter` instance
- Add rate limiting to the credential endpoints in `app/routes/credentials.py`
- Choose reasonable limits (e.g. "10/minute" or "100/hour")
- Make minimal changes
- Ensure the limiter is properly wired into the FastAPI app

Focus only on adding the decorators.