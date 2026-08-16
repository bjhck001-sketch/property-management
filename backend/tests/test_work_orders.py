"""Test work order endpoints"""
import pytest
from httpx import AsyncClient


class TestWorkOrders:
    """Test work order endpoints"""
    
    async def test_list_work_orders(self, client: AsyncClient, auth_headers: dict):
        """Test list work orders"""
        response = await client.get("/api/v1/work-orders/work-orders/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_create_work_order(self, client: AsyncClient, auth_headers: dict):
        """Test create work order"""
        response = await client.post(
            "/api/v1/work-orders/work-orders/",
            json={
                "property_id": 1,
                "order_type": "repair",
                "title": "Test Work Order",
                "description": "Test description",
                "priority": "medium"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Work Order"
        assert data["status"] == "pending"
    
    async def test_update_work_order(self, client: AsyncClient, admin_auth_headers: dict):
        """Test update work order"""
        # Create work order first
        create_response = await client.post(
            "/api/v1/work-orders/work-orders/",
            json={
                "property_id": 1,
                "order_type": "inspection",
                "title": "Inspection Task",
                "description": "Regular inspection",
                "priority": "low"
            },
            headers=admin_auth_headers
        )
        order_id = create_response.json()["id"]
        
        # Update work order
        response = await client.put(
            f"/api/v1/work-orders/work-orders/{order_id}",
            json={"status": "in_progress"},
            headers=admin_auth_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
    
    async def test_list_inspection_tasks(self, client: AsyncClient, auth_headers: dict):
        """Test list inspection tasks"""
        response = await client.get("/api/v1/work-orders/inspection-tasks/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    async def test_create_inspection_task(self, client: AsyncClient, admin_auth_headers: dict):
        """Test create inspection task (admin only)"""
        response = await client.post(
            "/api/v1/work-orders/inspection-tasks/",
            json={
                "property_id": 1,
                "inspector_id": 2,
                "task_name": "Elevator Inspection",
                "location": "Building 1"
            },
            headers=admin_auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["task_name"] == "Elevator Inspection"
    
    async def test_get_stats(self, client: AsyncClient, admin_auth_headers: dict):
        """Test get statistics"""
        response = await client.get("/api/v1/work-orders/stats/", headers=admin_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "today_repairs" in data
        assert "pending_orders" in data
        assert "overdue_bills" in data
    
    async def test_get_stats_unauthorized(self, client: AsyncClient, auth_headers: dict):
        """Test get statistics without admin role"""
        response = await client.get("/api/v1/work-orders/stats/", headers=auth_headers)
        assert response.status_code == 403
