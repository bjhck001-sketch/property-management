"""Test complaint endpoints"""
import pytest
from httpx import AsyncClient


class TestComplaints:
    """Test complaint endpoints"""
    
    async def _create_property(self, client: AsyncClient, auth_headers: dict) -> int:
        """Helper to create a property and return its ID"""
        response = await client.post(
            "/api/v1/properties/",
            json={
                "community_id": 1,
                "building_no": "1",
                "unit_no": "1",
                "floor_no": "1",
                "room_no": "101",
                "area": 100.0
            },
            headers=auth_headers
        )
        assert response.status_code == 201, f"Failed to create property: {response.text}"
        return response.json()["id"]
    
    async def test_create_complaint(self, client: AsyncClient, auth_headers: dict):
        """Test create complaint"""
        property_id = await self._create_property(client, auth_headers)
        
        response = await client.post(
            "/api/v1/complaints/",
            json={
                "property_id": property_id,
                "complaint_type": "service",
                "title": "Rude staff",
                "description": "Staff was rude during interaction"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Rude staff"
        assert data["status"] == "pending"
    
    async def test_list_complaints(self, client: AsyncClient, auth_headers: dict):
        """Test list complaints"""
        response = await client.get("/api/v1/complaints/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_get_complaint(self, client: AsyncClient, auth_headers: dict):
        """Test get complaint details"""
        property_id = await self._create_property(client, auth_headers)
        
        create_response = await client.post(
            "/api/v1/complaints/",
            json={
                "property_id": property_id,
                "complaint_type": "noise",
                "title": "Noise complaint",
                "description": "Loud music at night"
            },
            headers=auth_headers
        )
        assert create_response.status_code == 201
        complaint_id = create_response.json()["id"]
        
        # Get complaint
        response = await client.get(f"/api/v1/complaints/{complaint_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Noise complaint"
    
    async def test_update_complaint_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test update complaint (admin only)"""
        property_id = await self._create_property(client, admin_auth_headers)
        
        # Create complaint
        create_response = await client.post(
            "/api/v1/complaints/",
            json={
                "property_id": property_id,
                "complaint_type": "sanitation",
                "title": "Cleanliness issue",
                "description": "Garbage not collected"
            },
            headers=admin_auth_headers
        )
        assert create_response.status_code == 201
        
        complaint_id = create_response.json()["id"]
        
        # Update complaint
        response = await client.put(
            f"/api/v1/complaints/{complaint_id}",
            json={"status": "processing", "response": "We will address this"},
            headers=admin_auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "processing"
    
    async def test_update_complaint_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test update complaint without admin role"""
        response = await client.put(
            "/api/v1/complaints/1",
            json={"status": "completed"},
            headers=auth_headers
        )
        # Should be 403 (not allowed) or 404 (not found)
        assert response.status_code in [403, 404]
    
    async def test_get_complaint_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test get non-existent complaint"""
        response = await client.get("/api/v1/complaints/999", headers=auth_headers)
        assert response.status_code == 404
