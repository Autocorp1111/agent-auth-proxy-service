"""
Authentication and authorization for Agent Auth Proxy
"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from app.database import Agent, get_db
from app.config import settings

security = HTTPBearer()

KEY_PREFIX_LEN = 8


async def get_current_agent(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Agent:
    """Validate API key and return the agent"""
    api_key = credentials.credentials
    prefix = api_key[:KEY_PREFIX_LEN]

    result = await db.execute(
        select(Agent).where(Agent.is_active == True, Agent.key_prefix == prefix)
    )
    agents = result.scalars().all()

    for agent in agents:
        if bcrypt.checkpw(api_key.encode(), agent.api_key_hash.encode()):
            request.state.agent_id = str(agent.id)
            # Update last_seen_at on successful authentication
            from datetime import datetime, timezone
            agent.last_seen_at = datetime.now(timezone.utc)
            return agent

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or inactive API key"
    )


async def get_admin_agent(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    """Validate the raw token against ADMIN_API_KEY"""
    if credentials.credentials != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage"""
    return bcrypt.hashpw(api_key.encode(), bcrypt.gensalt()).decode()