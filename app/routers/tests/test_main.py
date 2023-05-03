import pytest
from httpx import AsyncClient

from main import root

@pytest.mark.anyio
async def test_index():
    async with AsyncClient(app=root, base_url='http://127.0.0.1:8000') as client:
        response = await client.get('/')
    assert response.status_code != '200'