import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

from app.orm.config import get_async_session
from app.orm.config import ORMModel
from app.app import app

load_dotenv()
driver = TEST_DATABASE_DRIVER = os.getenv("TEST_DATABASE_DRIVER")
user = TEST_DATABASE_USERNAME = os.getenv("TEST_DATABASE_USERNAME")
password = TEST_DATABASE_PASSWORD = os.getenv("TEST_DATABASE_PASSWORD")
host = TEST_DATABASE_HOSTNAME = os.getenv("TEST_DATABASE_HOSTNAME")
port = TEST_DATABASE_PORT = os.getenv("TEST_DATABASE_PORT")
name = TEST_DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")

# DATABASE
DATABASE_URL_TEST = f"{driver}://{user}:{password}@{host}:{port}/{name}"
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
ORMModel.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    try:
        async with engine_test.begin() as conn:
            await conn.run_sync(ORMModel.metadata.create_all)
        yield
    finally:
        async with engine_test.begin() as conn:
            await conn.run_sync(ORMModel.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
