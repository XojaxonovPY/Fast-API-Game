import json
import os
import sys
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from db.models import metadata
from db.sessions import get_db

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine_test = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_session


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture
def fake_redis(monkeypatch):
    storage = {}

    async def _get(key):
        return storage.get(key)

    async def _set(mapping):
        storage.update(mapping)

    async def _delete(key):
        storage.pop(key, None)

    monkeypatch.setattr("utils.settings.redis.get", _get)
    monkeypatch.setattr("utils.settings.redis.mset", _set)
    monkeypatch.setattr("utils.settings.redis.delete", _delete)
    return storage


async def login_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/login/token", json={
            "email": 'botir@gmail.com',
            "password": "1"
        })
        assert 200 <= response.status_code <= 400, 'User not registered'
        access_token = response.json().get('access_token')
        return access_token


@pytest.mark.asyncio
async def test_user_register_and_verify(fake_redis):
    with patch("apps.login_register.send_email_code.delay", return_value=None):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # 1) Register
            resp = await ac.post("login/user/register", json={
                "email": 'ali@gmail.com',
                "password": "1"
            })
            print(resp.json())
            assert resp.status_code == 200
            data = resp.json()
            pk = data["pk"]

            assert pk in fake_redis
            saved = json.loads(fake_redis[pk])

            # 2) Verify
            resp2 = await ac.post("/login/user/verify", json={
                "pk": pk,
                "code": saved["code"]
            })
            print(resp2.json())
            assert resp2.status_code == 200
            verified_user = resp2.json()
            assert verified_user["email"] == "ali@gmail.com"


@pytest.mark.asyncio
async def test_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await login_user()


@pytest.mark.asyncio
async def test_create_game():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await login_user()
        print(token)
        res = await client.post("/api/create/game/", json={
            'title': 'Game'
        }, headers={"Authorization": f"Bearer {token}"})
        assert 200 <= res.status_code <= 400


@pytest.mark.asyncio
async def test_list_game():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        token = await login_user()
        print(token)
        res = await client.get("/api/games/list/", headers={"Authorization": f"Bearer {token}"})
        assert 200 <= res.status_code <= 400


@pytest.mark.asyncio
async def test_create_question():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/create/question/", json={
            'text': 'question',
            'correct_answer': 'answer1',
            'game_id': '1'
        })
        assert 200 <= res.status_code <= 400


@pytest.mark.asyncio
async def test_create_options():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/create/options", json={
            'text': 'option',
            'question_id': '1'
        })
        assert 200 <= res.status_code <= 400


@pytest.mark.asyncio
async def test_list_question():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/questions/list/7216")
        assert 200 <= res.status_code <= 400


@pytest.mark.asyncio
async def test_list_options():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/options/list/1")
        assert 200 <= res.status_code <= 400
