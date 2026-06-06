# Contributing to Agent Auth Proxy

## Development Setup

1. Clone the repository
2. Create a `.env` file from `.env.example`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing
```bash
pytest tests/ -v
```

## Code Style
- Use `structlog` for all logging
- Keep Bitwarden logic isolated in `bitwarden.py`
- Write tests for new features

## Pull Requests
- Keep PRs focused and small
- Update documentation when changing behavior
- Ensure all tests pass