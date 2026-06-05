from fastapi import APIRouter, Request, Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.auth import get_current_agent
from app.database import Agent, AccessLog, CredentialAccess, get_db
from app.bitwarden import BitwardenClient
from app.dependencies import get_bitwarden_client
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/credentials", tags=["credentials"])


def get_agent_key(request: Request) -> str:
    return getattr(request.state, "agent_id", None) or get_remote_address(request)


limiter = Limiter(key_func=get_agent_key)


@router.get("/", response_model=List[str])
@limiter.limit("30/minute")
async def list_credentials(
    request: Request,
    agent: Agent = Depends(get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    """List credential names the agent has access to"""
    result = await db.execute(
        select(CredentialAccess.credential_name).where(CredentialAccess.agent_id == agent.id)
    )
    credentials = [row[0] for row in result.all()]
    return credentials


@router.get("/{name}")
@limiter.limit("10/minute")
async def get_credential(
    name: str,
    request: Request,
    agent: Agent = Depends(get_current_agent),
    bitwarden: BitwardenClient = Depends(get_bitwarden_client),
    db: AsyncSession = Depends(get_db)
):
    """Return the credential value if the agent has access"""
    # Check access
    result = await db.execute(
        select(CredentialAccess).where(
            CredentialAccess.agent_id == agent.id,
            CredentialAccess.credential_name == name
        )
    )
    access = result.scalar_one_or_none()
    if not access:
        raise HTTPException(status_code=403, detail="access_denied")

    success = False
    error_code = None
    value = None

    try:
        value = await bitwarden.get_credential(name)
        success = True
        logger.info("credential_access_success", agent_id=str(agent.id), credential=name)
    except Exception as e:
        error_code = str(e)
        logger.warning("credential_access_failed", agent_id=str(agent.id), credential=name, error=str(e))
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        try:
            log = AccessLog(
                agent_id=agent.id,
                credential_name=name,
                success=success,
                error_code=error_code
            )
            db.add(log)
            await db.commit()
        except Exception as log_err:
            logger.error("access_log_commit_failed", error=str(log_err))

    return {"name": name, "value": value}