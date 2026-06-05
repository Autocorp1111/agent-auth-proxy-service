# Agent Auth Proxy

Production-grade authentication proxy with Bitwarden integration for autonomous AI agents.

## Architecture

```
┌─────────────┐     ┌──────────────────────┐     ┌─────────────┐
│   Agents    │────▶│  Agent Auth Proxy    │────▶│  Bitwarden  │
│  (API Keys) │     │  (FastAPI + Alembic) │     │     CLI     │
└─────────────┘     └──────────────────────┘     └─────────────┘
                            │
                    ┌───────┴───────┐
                    │   PostgreSQL  │
                    └───────────────┘
```

## Key Features
- API key authentication with `last_seen_at` tracking
- Secure Bitwarden CLI integration (singleton pattern)
- Automatic database migrations on startup
- Admin endpoints for manual operations
- Structured logging and observability
- Rate limiting and security hardening

## Quick Start
```bash
uvicorn app.main:app --reload
```

## Testing
```bash
pytest tests/ -v
```

## Deployment
See `DEPLOYMENT.md` for Railway configuration and auto-migration details.