"""Test admin endpoints"""
import pytest
from httpx import AsyncClient


class TestAdmin:
    """Test admin endpoints"""
    
    async def test_list_users_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test list users (admin only)"""
        response = await client.get("/api/v1/admins/users/", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_list_users_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test list users without admin role"""
        response = await client.get("/api/v1/admins/users/", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_list_properties_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test list properties (admin only)"""
        response = await client.get("/api/v1/admins/properties/", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_list_properties_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test list properties without admin role"""
        response = await client.get("/api/v1/admins/properties/", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_list_communities(self, client: AsyncClient, admin_auth_headers: dict):
        """Test list communities"""
        response = await client.get("/api/v1/admins/communities/", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_get_stats_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test get statistics (admin only)"""
        response = await client.get("/api/v1/admins/stats/", headers=admin_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_properties" in data
        assert "total_communities" in data
        assert "unpaid_bills" in data
        assert "pending_repairs" in data
    
    async def test_get_stats_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test get statistics without admin role"""
        response = await client.get("/api/v1/admins/stats/", headers=auth_headers)
        assert response.status_code == 403
