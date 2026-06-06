# Agent Auth Proxy Operations Checklist

Use this checklist before merging, deploying, or handing the proxy to another agent/operator.

## Local readiness

- Run the test suite:
  ```bash
  .venv/bin/python -m pytest -q --tb=short
  ```
- Confirm no credential files are staged:
  ```bash
  git status --short
  git diff --cached --name-only
  ```
- Confirm `.gitignore` still excludes `.env`, `.env.*`, logs, caches, virtualenvs, and generated migration files except `migrations/versions/001_initial_tables.py`.

## Admin endpoint checks

- Admin-only endpoints require the `X-Admin-Key` header matching `ADMIN_API_KEY`.
- Register agents through `POST /agents/register`; duplicate agent names should return `409 Conflict`.
- Grant access through `POST /agents/{agent_id}/access/grant?credential_name=<name>`; unknown agents return `404`, duplicate grants return `409`.
- Revoke access through `POST /agents/{agent_id}/access/revoke?credential_name=<name>`; unknown agents or missing grants return `404`.
- Treat returned agent API keys as one-time secrets. Store them in the intended agent profile and do not commit them.

## Health checks

- `GET /health` should return `{"status":"ok"}` without auth.
- `GET /ready` should verify database and Bitwarden reachability before traffic is routed to the service.
- `GET /metrics` should stay protected according to the current metrics-auth policy; do not expose operational metrics publicly.
- Check logs for `request_id`, route, status code, auth failures, and Bitwarden failures after any smoke test.

## Bitwarden singleton behavior

- The FastAPI lifespan creates one `BitwardenClient` at `app.state.bitwarden`.
- Credential routes should depend on that application-scoped client, not instantiate new clients per request.
- Bitwarden CLI commands must receive `BW_MASTER_PASSWORD` through the subprocess environment only; do not pass the master password in argv or logs.
- Error logs from Bitwarden must stay sanitized before being emitted or returned to clients.

## Deployment notes

- Railway must provide `DATABASE_URL`, `BW_EMAIL`, `BW_MASTER_PASSWORD`, `BW_COLLECTION_ID`, `PROXY_MASTER_SECRET`, and `ADMIN_API_KEY`.
- Startup runs `alembic upgrade head`; check migration logs after each deploy.
- After deploy, perform a smoke test in this order: `/health`, `/ready`, admin register, grant access, credential retrieval from a permitted agent, revoke access, verify denied credential retrieval.

## Rollback criteria

Rollback or halt deployment if any of these occur:

- `/ready` reports database or Bitwarden failure.
- New agent registration returns a key but the key cannot authenticate.
- Credential access grants/revokes are not reflected in authorization decisions.
- Bitwarden errors expose secrets or unsanitized command output.
- Migration startup logs show failure against production database.
