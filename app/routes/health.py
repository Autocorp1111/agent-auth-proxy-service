from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import get_db
from app.dependencies import get_bitwarden_client
from app.bitwarden import BitwardenClient

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Basic health check for Railway"""
    return {"status": "ok"}


@router.get("/ready")
async def readiness_probe(
    request: Request,
    db: AsyncSession = Depends(get_db),
    bitwarden: BitwardenClient = Depends(get_bitwarden_client)
):
    """Readiness probe with dependency checks"""
    checks = {"database": False, "bitwarden": False}
    errors = {}

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception as e:
        errors["database"] = str(e)

    # Bitwarden check
    try:
        if bitwarden:
            checks["bitwarden"] = await bitwarden.ping()
        else:
            errors["bitwarden"] = "client_not_initialized"
    except Exception as e:
        errors["bitwarden"] = str(e)

    status = "ready" if all(checks.values()) else "not_ready"
    
    response = {"status": status, "checks": checks}
    if errors:
        response["errors"] = errors
    
    return response