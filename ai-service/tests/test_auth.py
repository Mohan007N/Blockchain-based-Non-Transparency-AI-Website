"""
Tests for authentication endpoints
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuth:
    """Test authentication functionality"""
    
    async def test_register_success(self, client: AsyncClient, sample_user_data: dict):
        """Test successful user registration"""
        response = await client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]
        assert "id" in data
        assert "hashed_password" not in data
    
    async def test_register_duplicate_email(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test registration with duplicate email"""
        # First registration
        await client.post("/api/auth/register", json=sample_user_data)
        
        # Second registration with same email
        response = await client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "password": "SecurePass123!",
                "name": "Test User"
            }
        )
        
        assert response.status_code == 422
    
    async def test_register_weak_password(self, client: AsyncClient):
        """Test registration with weak password"""
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "123",
                "name": "Test User"
            }
        )
        
        assert response.status_code == 422
    
    async def test_login_success(self, client: AsyncClient, sample_user_data: dict):
        """Test successful login"""
        # Register first
        await client.post("/api/auth/register", json=sample_user_data)
        
        # Login
        response = await client.post(
            "/api/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    async def test_login_wrong_password(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test login with wrong password"""
        # Register first
        await client.post("/api/auth/register", json=sample_user_data)
        
        # Login with wrong password
        response = await client.post(
            "/api/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": "WrongPassword123!"
            }
        )
        
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user"""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!"
            }
        )
        
        assert response.status_code == 401
    
    async def test_get_current_user(
        self,
        authenticated_client: tuple[AsyncClient, dict]
    ):
        """Test getting current user profile"""
        client, token_data = authenticated_client
        
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == token_data["user"]["email"]
        assert "hashed_password" not in data
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication"""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401
    
    async def test_update_profile(
        self,
        authenticated_client: tuple[AsyncClient, dict]
    ):
        """Test updating user profile"""
        client, _ = authenticated_client
        
        response = await client.patch(
            "/api/auth/me",
            json={"name": "Updated Name", "phone": "+1234567890"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["phone"] == "+1234567890"
