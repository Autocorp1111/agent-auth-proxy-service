# API Documentation

## Authentication
All endpoints (except `/health`) require a Bearer token.

## Endpoints

### Credentials
- `GET /credentials/` - List accessible credentials
- `GET /credentials/{name}` - Retrieve a specific credential

### Agents
- `POST /agents/register` - Register new agent (admin)
- `GET /agents/me` - Get current agent profile

## Error Codes
- `401` - Invalid API key
- `403` - Access denied
- `503` - Bitwarden service unavailable