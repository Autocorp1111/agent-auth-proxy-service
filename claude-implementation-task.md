# Implementation Task for Claude Code

**Project:** Agent Auth Proxy
**Goal:** Fix critical P0 issues and begin implementing production readiness tasks.

**Priority Tasks to Implement:**

1. Fix admin authorization in `app/auth.py` to properly validate `ADMIN_API_KEY`
2. Convert Bitwarden client to singleton pattern using `app.state`
3. Apply rate limiting decorators to credential endpoints
4. Implement real Bitwarden connectivity check in health endpoint
5. Wire Alembic migrations to run on Railway deployment
6. Fix exception handling around `AccessLog` commits
7. Update `last_seen_at` on successful authentication

**Instructions for Claude:**
- Work inside `/mnt/e/Agents/project/agent-auth-proxy`
- Make targeted, minimal changes
- Use existing patterns in the codebase
- After changes, briefly explain what was fixed
- Focus on making the application actually runnable and secure

Start with the highest priority P0 fixes.