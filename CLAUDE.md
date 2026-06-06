# Claude Code Instructions - Agent Auth Proxy

## Project Overview
Central credential proxy service that allows multiple AI agents to securely retrieve credentials from Bitwarden.

## Key Rules

- Only `bitwarden.py` is allowed to call the `bw` CLI
- All credential access must be logged
- Use structured logging (structlog) everywhere
- Never commit `.env` or real API keys

## Current Architecture
- FastAPI + SQLAlchemy (async)
- Bitwarden CLI integration with advanced error handling
- Per-agent API key authentication
- Admin endpoints for registration and access management

## Development Guidelines
- Follow the implementation plan in `Implementation_Agent_Auth_Proxy.md`
- Milestone 1 (Bitwarden Validation Gate) is a hard gate
- Prefer dependency injection via `app/dependencies.py`
- Use lifespan events instead of deprecated `@app.on_event`

## Next Priority
Focus on completing Milestone 2 (Credential Proxy Core) after Milestone 1 passes.