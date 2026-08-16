"""Test visitor endpoints"""
import pytest
from httpx import AsyncClient


class TestVisitors:
    """Test visitor endpoints"""
    
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
    
    async def test_create_visitor(self, client: AsyncClient, auth_headers: dict):
        """Test create visitor record"""
        from datetime import datetime, timedelta
        property_id = await self._create_property(client, auth_headers)
        
        response = await client.post(
            "/api/v1/visitors/",
            json={
                "property_id": property_id,
                "visitor_name": "John Doe",
                "visitor_phone": "13900139000",
                "start_time": datetime.utcnow().isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=4)).isoformat()
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["visitor_name"] == "John Doe"
        assert "access_code" in data
        assert len(data["access_code"]) == 8
    
    async def test_list_visitors(self, client: AsyncClient, auth_headers: dict):
        """Test list visitors"""
        response = await client.get("/api/v1/visitors/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_get_visitor(self, client: AsyncClient, auth_headers: dict):
        """Test get visitor details"""
        from datetime import datetime, timedelta
        property_id = await self._create_property(client, auth_headers)
        
        create_response = await client.post(
            "/api/v1/visitors/",
            json={
                "property_id": property_id,
                "visitor_name": "Jane Smith",
                "visitor_phone": "13900139001",
                "start_time": datetime.utcnow().isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat()
            },
            headers=auth_headers
        )
        assert create_response.status_code == 201
        visitor_id = create_response.json()["id"]
        
        # Get visitor
        response = await client.get(f"/api/v1/visitors/{visitor_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["visitor_name"] == "Jane Smith"
    
    async def test_check_in_visitor(self, client: AsyncClient, auth_headers: dict):
        """Test visitor check-in"""
        from datetime import datetime, timedelta
        property_id = await self._create_property(client, auth_headers)
        
        # Create visitor
        create_response = await client.post(
            "/api/v1/visitors/",
            json={
                "property_id": property_id,
                "visitor_name": "Check-in Test",
                "visitor_phone": "13900139002",
                "start_time": datetime.utcnow().isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat()
            },
            headers=auth_headers
        )
        assert create_response.status_code == 201
        visitor_id = create_response.json()["id"]
        
        # Check-in (should fail as visitor is not approved)
        response = await client.post(
            f"/api/v1/visitors/{visitor_id}/check-in",
            headers=auth_headers
        )
        # Should fail because status is PENDING, not APPROVED
        assert response.status_code == 400
    
    async def test_get_visitor_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test get non-existent visitor"""
        response = await client.get("/api/v1/visitors/999", headers=auth_headers)
        assert response.status_code == 404
