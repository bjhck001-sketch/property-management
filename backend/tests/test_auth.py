"""Test authentication endpoints"""
import pytest
from httpx import AsyncClient


class TestAuth:
    """Test authentication endpoints"""
    
    async def test_register_success(self, client: AsyncClient):
        """Test user registration"""
        response = await client.post("/api/v1/auth/register", json={
            "phone": "13800138003",
            "password": "testpass123",
            "role": "owner",
            "name": "New User"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "13800138003"
        assert data["role"] == "owner"
        assert "id" in data
        assert "created_at" in data
    
    async def test_register_duplicate_phone(self, client: AsyncClient):
        """Test registration with duplicate phone"""
        # Register first user
        await client.post("/api/v1/auth/register", json={
            "phone": "13800138004",
            "password": "testpass123",
            "role": "owner",
            "name": "Duplicate Test"
        })
        
        # Try to register with same phone
        response = await client.post("/api/v1/auth/register", json={
            "phone": "13800138004",
            "password": "testpass123",
            "role": "owner",
            "name": "Duplicate Test 2"
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    async def test_login_success(self, client: AsyncClient):
        """Test user login"""
        # Register user first
        await client.post("/api/v1/auth/register", json={
            "phone": "13800138005",
            "password": "testpass123",
            "role": "owner",
            "name": "Login Test"
        })
        
        # Login
        response = await client.post("/api/v1/auth/login", json={
            "phone": "13800138005",
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_wrong_password(self, client: AsyncClient):
        """Test login with wrong password"""
        # Register user first
        await client.post("/api/v1/auth/register", json={
            "phone": "13800138006",
            "password": "testpass123",
            "role": "owner",
            "name": "Wrong Password Test"
        })
        
        # Login with wrong password
        response = await client.post("/api/v1/auth/login", json={
            "phone": "13800138006",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "phone or password" in response.json()["detail"].lower()
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user"""
        response = await client.post("/api/v1/auth/login", json={
            "phone": "13800138999",
            "password": "testpass123"
        })
        assert response.status_code == 401
    
    async def test_get_me(self, client: AsyncClient, auth_headers: dict):
        """Test get current user info"""
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "13800138001"
        assert "id" in data
    
    async def test_get_me_unauthorized(self, client: AsyncClient):
        """Test get current user without auth"""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 403
    
    async def test_logout(self, client: AsyncClient, auth_headers: dict):
        """Test logout"""
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        assert "message" in response.json()
    
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    async def test_root(self, client: AsyncClient):
        """Test root endpoint"""
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
