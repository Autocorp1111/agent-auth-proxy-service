# Claude Code Task: Alembic Migrations Setup

## Goal
Add proper database migration support using Alembic for the Agent Auth Proxy.

## Requirements
1. Initialize Alembic in the project
2. Create initial migration for existing models
3. Configure `alembic.ini` and `env.py`
4. Update `railway.toml` or `Dockerfile` if needed for migration runs

## Acceptance Criteria
- `alembic upgrade head` works cleanly
- All current models (`Agent`, `CredentialAccess`, `AccessLog`, `Task`) are covered
- Migration can be run in Railway environment

## Notes
This is a prerequisite for Milestone 2.