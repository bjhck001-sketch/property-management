"""Test property management endpoints"""
import pytest
from httpx import AsyncClient


class TestProperties:
    """Test property management endpoints"""
    
    async def test_create_property(self, client: AsyncClient, auth_headers: dict):
        """Test create property"""
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
        assert response.status_code == 201
        data = response.json()
        assert data["room_no"] == "101"
        assert data["area"] == 100.0
        assert "id" in data
    
    async def test_list_properties(self, client: AsyncClient, auth_headers: dict):
        """Test list user properties"""
        response = await client.get("/api/v1/properties/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_get_property(self, client: AsyncClient, auth_headers: dict):
        """Test get property details"""
        # Create property first
        create_response = await client.post(
            "/api/v1/properties/",
            json={
                "community_id": 1,
                "building_no": "2",
                "unit_no": "1",
                "floor_no": "2",
                "room_no": "201",
                "area": 80.0
            },
            headers=auth_headers
        )
        property_id = create_response.json()["id"]
        
        # Get property
        response = await client.get(f"/api/v1/properties/{property_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["room_no"] == "201"
    
    async def test_update_property(self, client: AsyncClient, auth_headers: dict):
        """Test update property"""
        # Create property first
        create_response = await client.post(
            "/api/v1/properties/",
            json={
                "community_id": 1,
                "building_no": "3",
                "unit_no": "1",
                "floor_no": "3",
                "room_no": "301",
                "area": 90.0
            },
            headers=auth_headers
        )
        property_id = create_response.json()["id"]
        
        # Update property
        response = await client.put(
            f"/api/v1/properties/{property_id}",
            json={"area": 95.0},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["area"] == 95.0
    
    async def test_delete_property(self, client: AsyncClient, auth_headers: dict):
        """Test delete property"""
        # Create property first
        create_response = await client.post(
            "/api/v1/properties/",
            json={
                "community_id": 1,
                "building_no": "4",
                "unit_no": "1",
                "floor_no": "4",
                "room_no": "401",
                "area": 70.0
            },
            headers=auth_headers
        )
        property_id = create_response.json()["id"]
        
        # Delete property
        response = await client.delete(f"/api/v1/properties/{property_id}", headers=auth_headers)
        assert response.status_code == 204
    
    async def test_get_property_not_found(self, client: AsyncClient, auth_headers: dict):
        """Test get non-existent property"""
        response = await client.get("/api/v1/properties/999", headers=auth_headers)
        assert response.status_code == 404
    
    async def test_unauthorized(self, client: AsyncClient):
        """Test unauthorized access"""
        response = await client.get("/api/v1/properties/")
        assert response.status_code == 403
