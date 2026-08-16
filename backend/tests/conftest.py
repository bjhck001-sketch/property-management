"""Test configuration for property management backend"""
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport

pytest_plugins = ("pytest_asyncio",)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db
from src.models.user import User
from src.middleware import get_password_hash
import os
from dotenv import load_dotenv

load_dotenv(".env.test")


# Test database URL
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")


# Create test engine
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in TEST_DATABASE_URL else None,
)

AsyncTestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    """Override database dependency for testing"""
    async with AsyncTestSession() as session:
        try:
            yield session
        finally:
            await session.close()


# Setup and teardown - use function scope for isolation
@pytest.fixture(scope="function")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown_db(event_loop):
    """Setup and teardown database for each test"""
    # Setup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Yield to tests
    yield
    
    # Teardown - drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def client(event_loop):
    """Create test client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(scope="function")
async def test_user(client: AsyncClient):
    """Create a test user"""
    response = await client.post("/api/v1/auth/register", json={
        "phone": "13800138001",
        "password": "testpass123",
        "role": "owner",
        "name": "Test User"
    })
    if response.status_code == 400:
        pass
    return response.json()


@pytest.fixture(scope="function")
async def test_admin(client: AsyncClient):
    """Create a test admin"""
    response = await client.post("/api/v1/auth/register", json={
        "phone": "13800138002",
        "password": "adminpass123",
        "role": "admin",
        "name": "Test Admin"
    })
    if response.status_code == 400:
        pass
    return response.json()


@pytest.fixture(scope="function")
async def auth_headers(client: AsyncClient, test_user: dict):
    """Get auth headers for test user"""
    response = await client.post("/api/v1/auth/login", json={
        "phone": "13800138001",
        "password": "testpass123"
    })
    assert response.status_code == 200, f"User login failed: {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def admin_auth_headers(client: AsyncClient, test_admin: dict):
    """Get auth headers for admin user"""
    response = await client.post("/api/v1/auth/login", json={
        "phone": "13800138002",
        "password": "adminpass123"
    })
    assert response.status_code == 200, f"Admin login failed: {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
