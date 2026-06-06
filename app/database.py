"""
Database models and session factory for Agent Auth Proxy
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from datetime import datetime, timezone
import uuid

from app.config import settings

# Async engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass


class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    api_key_hash = Column(String, nullable=False)
    key_prefix = Column(String(8), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CredentialAccess(Base):
    __tablename__ = "credential_access"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    credential_name = Column(String, nullable=False, index=True)
    granted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    credential_name = Column(String, nullable=False)
    accessed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    success = Column(Boolean, nullable=False)
    error_code = Column(String, nullable=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    payload = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))