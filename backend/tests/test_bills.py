"""Test bill management endpoints"""
import pytest
from httpx import AsyncClient


class TestBills:
    """Test bill management endpoints"""
    
    async def test_list_bills_empty(self, client: AsyncClient, auth_headers: dict):
        """Test list bills when empty"""
        response = await client.get("/api/v1/bills/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_bill_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test create bill (admin only)"""
        from datetime import datetime, timedelta
        response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 500.0,
                "period": "2024-01",
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            headers=admin_auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 500.0
        assert data["status"] == "pending"
    
    async def test_create_bill_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test create bill without admin role"""
        response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 500.0,
                "period": "2024-01",
                "due_date": "2024-02-01T00:00:00"
            },
            headers=auth_headers
        )
        assert response.status_code == 403
    
    async def test_get_bill(self, client: AsyncClient, admin_auth_headers: dict):
        """Test get bill details"""
        # Create bill first
        from datetime import datetime, timedelta
        create_response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 600.0,
                "period": "2024-02",
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            headers=admin_auth_headers
        )
        bill_id = create_response.json()["id"]
        
        # Get bill
        response = await client.get(f"/api/v1/bills/{bill_id}", headers=admin_auth_headers)
        assert response.status_code == 200
        assert response.json()["amount"] == 600.0
    
    async def test_batch_generate_bills(self, client: AsyncClient, admin_auth_headers: dict):
        """Test batch generate bills"""
        # Create some properties first
        await client.post(
            "/api/v1/properties/",
            json={
                "community_id": 1,
                "building_no": "1",
                "unit_no": "1",
                "floor_no": "1",
                "room_no": "101",
                "area": 100.0
            },
            headers=admin_auth_headers
        )
        
        response = await client.post("/api/v1/bills/batch-generate", headers=admin_auth_headers)
        assert response.status_code == 200
        assert len(response.json()) > 0
        for bill in response.json():
            assert bill["status"] == "pending"
    
    async def test_get_bill_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test get non-existent bill"""
        response = await client.get("/api/v1/bills/999", headers=admin_auth_headers)
        assert response.status_code == 404
