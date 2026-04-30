"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.sqlite_db import Base, get_db
from main import app


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override"""
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user registration data"""
    return {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User",
        "role": "client"
    }


@pytest.fixture
def sample_loan_data():
    """Sample loan verification data"""
    return {
        "loanType": "personal",
        "extractedData": {
            "creditScore": 720,
            "monthlyIncome": 45000,
            "age": 28,
            "workExperienceYears": 3,
            "debtToIncomeRatio": 0.30,
            "loanAmount": 500000
        }
    }


@pytest.fixture
async def authenticated_client(
    client: AsyncClient,
    sample_user_data: dict
) -> AsyncGenerator[tuple[AsyncClient, dict], None]:
    """Create authenticated client with JWT token"""
    
    # Register user
    response = await client.post("/api/auth/register", json=sample_user_data)
    assert response.status_code == 201
    
    # Login
    login_response = await client.post(
        "/api/auth/login",
        json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    assert login_response.status_code == 200
    
    token_data = login_response.json()
    token = token_data["access_token"]
    
    # Set authorization header
    client.headers["Authorization"] = f"Bearer {token}"
    
    yield client, token_data
    
    # Cleanup
    client.headers.pop("Authorization", None)


@pytest.fixture
def mock_blockchain_service(monkeypatch):
    """Mock blockchain service for testing"""
    
    class MockBlockchainService:
        enabled = True
        
        async def record_verification(self, *args, **kwargs):
            return "0x1234567890abcdef"
        
        async def get_verification(self, verification_id):
            return {
                "user_id": "test-user",
                "data_hash": "0xabcdef",
                "status": "approved",
                "timestamp": 1234567890,
                "exists": True
            }
        
        async def update_status(self, verification_id, new_status):
            return "0xfedcba0987654321"
    
    from app.blockchain import contract
    monkeypatch.setattr(contract, "blockchain_service", MockBlockchainService())
    
    return MockBlockchainService()
