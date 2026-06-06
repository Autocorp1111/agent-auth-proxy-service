# Deployment Guide - Agent Auth Proxy

## Railway Deployment

### Current Issues
- Service is crashing with "Could not import module 'main'"
- Root cause: Railway using incorrect start command

### Required Configuration
- `railway.toml` must contain explicit `startCommand`
- `Procfile` should also define the correct command

### Recommended Start Command
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Health Checks
- `/health` endpoint available
- Configure Railway health check to use this endpoint

## Environment Variables
All required variables are documented in `.env.example`.
## Automatic Database Migrations

As of June 2026, the application now runs Alembic migrations automatically on startup.

### Behavior
- Migrations run during the FastAPI lifespan startup
- This ensures the database schema is always up to date on Railway
- Migrations are also available via the admin endpoint: `POST /admin/migrate`

### Monitoring
- Successful migrations are logged with structured output
- Failed migrations will log warnings/errors but will not crash the app
- Check logs for `alembic_migrations_applied` or `alembic_migration_failed`

### Manual Trigger
If needed, admins can manually trigger migrations using the protected endpoint above.
