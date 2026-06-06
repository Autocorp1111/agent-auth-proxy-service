import pytest
from unittest.mock import AsyncMock, patch
from app.bitwarden import BitwardenClient, BitwardenUnavailableError


@pytest.mark.asyncio
async def test_bitwarden_client_initialization():
    client = BitwardenClient(
        email="test@example.com",
        master_password="testpass",
        collection_id="test-collection"
    )
    assert client.email == "test@example.com"


@pytest.mark.asyncio
async def test_bitwarden_error_handling():
    client = BitwardenClient("test", "test", "test")
    with patch.object(client, '_run_bw', return_value=(1, "", "error")):
        with pytest.raises(BitwardenUnavailableError):
            await client.get_credential("test-item")