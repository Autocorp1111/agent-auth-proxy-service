from contextlib import asynccontextmanager
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.bitwarden import BitwardenClient
from app.config import settings
from app.logging_config import configure_logging
from app.metrics import router as metrics_router
from app.routes import agents, credentials, health, admin
from app.routes.credentials import limiter

configure_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run Alembic migrations on startup (Railway production)
    import subprocess
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            logger.info(
                "alembic_migrations_applied",
                stdout=result.stdout.strip() if result.stdout else None
            )
        else:
            logger.warning(
                "alembic_migration_warning",
                returncode=result.returncode,
                stderr=result.stderr.strip() if result.stderr else None
            )
    except Exception as e:
        logger.error("alembic_migration_failed", error=str(e))

    app.state.bitwarden = BitwardenClient(
        email=settings.BW_EMAIL,
        master_password=settings.BW_MASTER_PASSWORD,
        collection_id=settings.BW_COLLECTION_ID,
    )
    logger.info("bitwarden_client_initialized")
    yield
    logger.info("shutdown")


app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(health.router)
app.include_router(credentials.router)
app.include_router(agents.router)
app.include_router(metrics_router)
app.include_router(admin.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        request_id=request_id,
    )
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        request_id=request_id,
    )
    return response
