# Rate Limiting

The Agent Auth Proxy uses `slowapi` for rate limiting.

## Default Limits
- 100 requests per minute per IP by default
- Can be adjusted per endpoint

## Configuration
Rate limiting is configured in `main.py` using the Limiter from slowapi.

## Headers
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `Retry-After` (when limited)