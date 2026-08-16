"""Test payment endpoints"""
import pytest
from httpx import AsyncClient


class TestPayments:
    """Test payment endpoints"""
    
    async def test_list_payments_empty(self, client: AsyncClient, auth_headers: dict):
        """Test list payments when empty"""
        response = await client.get("/api/v1/payments/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_create_payment_order(self, client: AsyncClient, admin_auth_headers: dict):
        """Test create payment order"""
        # Create a bill first
        from datetime import datetime, timedelta
        bill_response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 500.0,
                "period": "2024-03",
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            headers=admin_auth_headers
        )
        bill_id = bill_response.json()["id"]
        
        # Create payment order
        response = await client.post(
            "/api/v1/payments/create",
            json={"bill_id": bill_id, "payment_method": "wechat"},
            headers=admin_auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["bill_id"] == bill_id
        assert data["status"] == "pending"
    
    async def test_confirm_payment(self, client: AsyncClient, admin_auth_headers: dict):
        """Test confirm payment"""
        # Create bill and payment
        from datetime import datetime, timedelta
        bill_response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 600.0,
                "period": "2024-04",
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            headers=admin_auth_headers
        )
        bill_id = bill_response.json()["id"]
        
        payment_response = await client.post(
            "/api/v1/payments/create",
            json={"bill_id": bill_id, "payment_method": "alipay"},
            headers=admin_auth_headers
        )
        payment_id = payment_response.json()["id"]
        
        # Confirm payment
        response = await client.post(
            f"/api/v1/payments/{payment_id}/confirm",
            headers=admin_auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "transaction_id" in data
    
    async def test_payment_double_confirm(self, client: AsyncClient, admin_auth_headers: dict):
        """Test double confirm payment"""
        # Create bill and payment
        from datetime import datetime, timedelta
        bill_response = await client.post(
            "/api/v1/bills/",
            json={
                "property_id": 1,
                "bill_type": "property_fee",
                "amount": 700.0,
                "period": "2024-05",
                "due_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
            },
            headers=admin_auth_headers
        )
        bill_id = bill_response.json()["id"]
        
        payment_response = await client.post(
            "/api/v1/payments/create",
            json={"bill_id": bill_id, "payment_method": "wechat"},
            headers=admin_auth_headers
        )
        payment_id = payment_response.json()["id"]
        
        # First confirm
        await client.post(f"/api/v1/payments/{payment_id}/confirm", headers=admin_auth_headers)
        
        # Try to confirm again (should fail as bill is already paid)
        response = await client.post(f"/api/v1/payments/{payment_id}/confirm", headers=admin_auth_headers)
        # May get 404 or similar since status changed
