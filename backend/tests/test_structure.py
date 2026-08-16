"""Test property management backend"""
import pytest
from pathlib import Path


def test_project_structure():
    """Test that required project structure exists"""
    base = Path(__file__).parent.parent
    
    # Check main files exist
    assert (base / "src" / "main.py").exists()
    assert (base / "src" / "config.py").exists()
    assert (base / "src" / "database.py").exists()
    assert (base / "src" / "middleware.py").exists()
    assert (base / "requirements.txt").exists()
    assert (base / "Dockerfile").exists()


def test_models_exist():
    """Test that all models are defined"""
    from src.models import (
        User, Community, Property, Bill, Payment,
        Repair, Visitor, Complaint, Notification,
        WorkOrder, InspectionTask
    )
    
    assert User is not None
    assert Community is not None
    assert Property is not None
    assert Bill is not None
    assert Payment is not None
    assert Repair is not None
    assert Visitor is not None
    assert Complaint is not None
    assert Notification is not None
    assert WorkOrder is not None
    assert InspectionTask is not None


def test_schemas_exist():
    """Test that all schemas are defined"""
    from src.schemas import (
        UserCreate, UserResponse, PropertyCreate, PropertyResponse,
        BillCreate, BillResponse, PaymentCreate, PaymentResponse,
        RepairCreate, RepairResponse, VisitorCreate, VisitorResponse,
        ComplaintCreate, ComplaintResponse, NotificationCreate,
        NotificationResponse, WorkOrderCreate, WorkOrderResponse
    )
    
    assert UserCreate is not None
    assert PropertyCreate is not None
    assert BillCreate is not None
    assert PaymentCreate is not None
    assert RepairCreate is not None
    assert VisitorCreate is not None
    assert ComplaintCreate is not None
    assert NotificationCreate is not None
    assert WorkOrderCreate is not None


def test_routers_exist():
    """Test that all routers are defined"""
    from src.routers import (
        auth, users, properties, bills, payments,
        repairs, visitors, complaints, notifications,
        work_orders, admins
    )
    
    assert auth is not None
    assert users is not None
    assert properties is not None
    assert bills is not None
    assert payments is not None
    assert repairs is not None
    assert visitors is not None
    assert complaints is not None
    assert notifications is not None
    assert work_orders is not None
    assert admins is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
