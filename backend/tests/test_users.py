"""Test user management endpoints"""
import pytest
from httpx import AsyncClient


class TestUsers:
    """Test user management endpoints"""
    
    async def test_get_profile(self, client: AsyncClient, auth_headers: dict):
        """Test get user profile"""
        response = await client.get("/api/v1/users/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "13800138001"
        assert data["name"] == "Test User"
    
    async def test_update_profile(self, client: AsyncClient, auth_headers: dict):
        """Test update user profile"""
        response = await client.put(
            "/api/v1/users/profile",
            json={"name": "Updated Name"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
    
    async def test_list_users_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test list users (admin only)"""
        response = await client.get("/api/v1/users/", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_list_users_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test list users without admin role"""
        response = await client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_get_user_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test get user by ID (admin only)"""
        response = await client.get("/api/v1/users/1", headers=admin_auth_headers)
        assert response.status_code == 200
        assert "id" in response.json()
    
    async def test_get_user_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test get user by ID without admin role"""
        response = await client.get("/api/v1/users/1", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_update_user_status(self, client: AsyncClient, admin_auth_headers: dict):
        """Test update user status (admin only)"""
        response = await client.put(
            "/api/v1/users/1/status?status=false",
            headers=admin_auth_headers
        )
        assert response.status_code == 200
        assert "message" in response.json()
