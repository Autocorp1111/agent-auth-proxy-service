import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Set required env vars before any app imports trigger config loading
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("BW_EMAIL", "test@example.com")
os.environ.setdefault("BW_MASTER_PASSWORD", "test-master-password")
os.environ.setdefault("BW_COLLECTION_ID", "test-collection-id")
os.environ.setdefault("PROXY_MASTER_SECRET", "test-proxy-secret")
os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")

from app.database import Base


@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        yield session

    await engine.dispose()