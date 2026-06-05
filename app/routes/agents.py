from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import secrets

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
    agent_id: str,
    credential_name: str,
    admin: bool = Depends(get_admin_agent),
    db: AsyncSession = Depends(get_db)
):
    """Grant an agent access to a credential"""
    access = CredentialAccess(agent_id=agent_id, credential_name=credential_name)
    db.add(access)
    await db.commit()
    return {"status": "granted", "agent_id": agent_id, "credential": credential_name}


@router.post("/{agent_id}/access/revoke")
async def revoke_credential_access(
    agent_id: str,
    credential_name: str,
    admin: bool = Depends(get_admin_agent),
    db: AsyncSession = Depends(get_db)
):
    """Revoke an agent's access to a credential"""
    await db.execute(
        delete(CredentialAccess).where(
            CredentialAccess.agent_id == agent_id,
            CredentialAccess.credential_name == credential_name
        )
    )
    await db.commit()
    return {"status": "revoked", "agent_id": agent_id, "credential": credential_name}