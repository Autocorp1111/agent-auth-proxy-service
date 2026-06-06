"""Admin-only endpoints for Agent Auth Proxy"""

from fastapi import APIRouter, Depends, HTTPException
import subprocess
import structlog

from app.auth import get_admin_agent

router = APIRouter(prefix="/admin", tags=["admin"])
logger = structlog.get_logger(__name__)


@router.post("/migrate", dependencies=[Depends(get_admin_agent)])
async def trigger_migration():
    """Manually trigger Alembic migrations (admin only)"""
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            logger.info("admin_migration_triggered", stdout=result.stdout)
            return {
                "status": "success",
                "message": "Migrations applied successfully",
                "output": result.stdout.strip()
            }
        else:
            logger.warning("admin_migration_failed", stderr=result.stderr)
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Migration failed",
                    "stderr": result.stderr.strip()
                }
            )
            
    except Exception as e:
        logger.error("admin_migration_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))