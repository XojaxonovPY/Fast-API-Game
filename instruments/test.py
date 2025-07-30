import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from db.models import metadata, User
from db.sessions import get_db  # get_db -> session
from db import engine as main_engine  # Real engine

# 🧪 Test uchun yangi engine (main_engine'ni buzmaslik uchun)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine_test = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)


# 🔁 Depends override qilish
async def override_get_session():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_session


# 🔧 Test DB yaratish va tozalash
@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# 🧪 Asosiy test
@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("api/games/list/")
        assert response.status_code == 200
