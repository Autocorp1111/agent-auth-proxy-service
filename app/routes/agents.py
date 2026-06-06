from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import secrets
from uuid import UUID

from app.auth import get_current_agent, get_admin_agent, hash_api_key, KEY_PREFIX_LEN
from app.database import Agent, CredentialAccess, get_db
from app.dependencies import get_bitwarden_client
from app.config import settings

router = APIRouter(prefix="/agents", tags=["agents"])


class RegisterAgentRequest(BaseModel):
    name: str


@router.post("/register")
async def register_agent(
    payload: RegisterAgentRequest,
    admin: bool = Depends(get_admin_agent),
    db: AsyncSession = Depends(get_db)
):
    """Admin endpoint to register a new agent"""
    existing = await db.execute(select(Agent).where(Agent.name == payload.name))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent with name '{payload.name}' already exists"
        )

    api_key = secrets.token_urlsafe(32)
    api_key_hash = hash_api_key(api_key)

    agent = Agent(name=payload.name, api_key_hash=api_key_hash, key_prefix=api_key[:KEY_PREFIX_LEN])
    db.add(agent)
    await db.commit()
    await db.refresh(agent)

    return {
        "id": str(agent.id),
        "name": agent.name,
        "api_key": api_key,
        "message": "Store this API key securely. It will not be shown again."
    }


@router.get("/me")
async def get_my_agent(agent: Agent = Depends(get_current_agent)):
    """Return the calling agent's profile"""
    return {
        "id": str(agent.id),
        "name": agent.name,
        "is_active": agent.is_active,
        "last_seen_at": agent.last_seen_at
    }


@router.post("/{agent_id}/access/grant")
async def grant_credential_access(
    agent_id: UUID,
    credential_name: str,
    admin: bool = Depends(get_admin_agent),
    db: AsyncSession = Depends(get_db)
):
    """Grant an agent access to a credential"""
    agent = await db.execute(select(Agent).where(Agent.id == agent_id))
    if agent.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )

    existing_access = await db.execute(
        select(CredentialAccess).where(
            CredentialAccess.agent_id == agent_id,
            CredentialAccess.credential_name == credential_name,
        )
    )
    if existing_access.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent '{agent_id}' already has access to '{credential_name}'"
        )

    access = CredentialAccess(agent_id=agent_id, credential_name=credential_name)
    db.add(access)
    await db.commit()
    return {"status": "granted", "agent_id": str(agent_id), "credential": credential_name}


@router.post("/{agent_id}/access/revoke")
async def revoke_credential_access(
    agent_id: UUID,
    credential_name: str,
    admin: bool = Depends(get_admin_agent),
    db: AsyncSession = Depends(get_db)
):
    """Revoke an agent's access to a credential"""
    agent = await db.execute(select(Agent).where(Agent.id == agent_id))
    if agent.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )

    result = await db.execute(
        delete(CredentialAccess).where(
            CredentialAccess.agent_id == agent_id,
            CredentialAccess.credential_name == credential_name,
        )
    )
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No access grant found for agent '{agent_id}' and credential '{credential_name}'"
        )
    await db.commit()
    return {"status": "revoked", "agent_id": str(agent_id), "credential": credential_name}
