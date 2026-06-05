# Claude Code Task: Milestone 2 - Credential Proxy Core

## Goal
Complete the core credential proxy functionality after Milestone 1 is cleared.

## Prerequisites
- Milestone 1 (Bitwarden Validation Gate) must be passed
- `bitwarden.py` must be stable

## Tasks
1. Set up Alembic migrations
2. Implement full authentication flow
3. Finalize credential endpoints with proper error handling
4. Add rate limiting using slowapi
5. Ensure all logging uses structlog correctly

## Acceptance Criteria
- Agents can register and authenticate
- Agents can request credentials they have access to
- All access is logged
- Rate limiting is active

## Notes
Do not proceed to Milestone 3 until this is complete.