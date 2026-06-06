# Security Guidelines - Agent Auth Proxy

## Credential Handling
- Never log raw credential values
- All access must be logged via `AccessLog` model
- Only `bitwarden.py` may call the `bw` CLI

## API Keys
- API keys are stored as bcrypt hashes
- Keys are only shown once during registration
- Admin operations require valid admin authentication

## Environment Variables
- Never commit `.env` or real secrets
- Use `.env.example` as the template

## Logging
- Use structlog for all logging
- Never include sensitive data in logs

## Deployment
- Keep `railway.toml` and `Dockerfile` up to date
- Regularly rotate master Bitwarden password
## Admin Endpoints
- `POST /admin/migrate` — Manually trigger database migrations (requires admin key)
- All admin endpoints are protected by `ADMIN_API_KEY`

## Rate Limiting
- Credential endpoints are rate-limited
- Admin endpoints should be used sparingly
