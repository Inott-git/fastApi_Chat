import pytest
from httpx import AsyncClient
from pymongo import MongoClient
from main import root
import app.config as cfg
from app import db, chats


@pytest.fixture()
async def create_app():
    root.mongodb_client = MongoClient(cfg.ATLAS_URI)
    root.database = root.mongodb_client[cfg.DB_NAME]
    root.manager = chats.settings.ConnectionManager(root.database)
    root.db_session = db.database.get_db()
    yield
    root.mongodb_client.close()
    root.db_session.close()


@pytest.mark.anyio
async def test_index_chat():
    async with AsyncClient(app=root, base_url='http://127.0.0.1:8000/') as client:
        response = await client.get('/chats')
    assert response.status_code == 307


@pytest.mark.usefixtures('create_app')
@pytest.mark.anyio
async def test_hist_chat():
    async with AsyncClient(app=root, base_url='https://127.0.0.1:8000') as client:
        form_data = {'chat_id': '6447f0524fccbd5a3d53236f'}
        await client.post('/chats/hist', data=form_data)


