# Claude Task: Fix Rate Limiter Key Function

**Project:** Agent Auth Proxy
**Scope:** Single focused fix

**Task:**
Fix the rate limiter key function so it correctly identifies the agent instead of failing or falling back to IP.

The current `get_agent_key` uses FastAPI Depends, which doesn't work with slowapi's key_func.

**Requirements:**
- Use request.state or a middleware to store the agent ID after authentication
- Update the key function to read from request.state
- Make minimal changes

Focus only on fixing the rate limiter key.