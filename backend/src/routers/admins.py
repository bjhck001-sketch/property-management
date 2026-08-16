from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json
from src.database import get_db
from src.models.user import User
from src.models.community import Community, Property
from src.models.bill import Bill, BillType, BillStatus
from src.models.repair import Repair, RepairType, RepairStatus
from src.models.work_order import WorkOrder, WorkOrderType, WorkOrderStatus, Priority, InspectionTask
from src.models.notification import Notification, NotificationType
from src.models.visitor import Visitor
from src.schemas.user import UserResponse
from src.schemas.bill import BillCreate, BillResponse
from src.schemas.repair import RepairCreate, RepairResponse
from src.schemas.work_order import WorkOrderCreate, WorkOrderResponse, InspectionTaskCreate, InspectionTaskResponse
from src.schemas.notification import NotificationCreate, NotificationResponse
from src.schemas.community import CommunityCreate, CommunityResponse, PropertyCreate, PropertyResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole
from datetime import datetime, date

router = APIRouter(tags=["Admin"])


@router.post("/communities/", response_model=CommunityResponse, status_code=status.HTTP_201_CREATED)
async def create_community(
    community_create: CommunityCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Create a new community (admin only)"""
    community = Community(**community_create.model_dump())
    db.add(community)
    await db.commit()
    await db.refresh(community)
    return community


@router.get("/communities/", response_model=List[CommunityResponse])
async def list_communities(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """List all communities (admin only)"""
    result = await db.execute(
        select(Community).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.post("/properties/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_create: PropertyCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Create a new property (admin only)"""
    property_obj = Property(**property_create.model_dump())
    db.add(property_obj)
    await db.commit()
    await db.refresh(property_obj)
    return property_obj


@router.get("/properties/", response_model=List[PropertyResponse])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """List all properties (admin only)"""
    result = await db.execute(
        select(Property).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/stats/", response_model=dict)
async def get_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Get system statistics (admin only)"""
    from sqlalchemy import func
    
    user_count = await db.execute(select(func.count()).select_from(User))
    property_count = await db.execute(select(func.count()).select_from(Property))
    community_count = await db.execute(select(func.count()).select_from(Community))
    
    unpaid_bills = await db.execute(
        select(func.count()).where(Bill.status == BillStatus.PENDING)
    )
    
    pending_repairs = await db.execute(
        select(func.count()).where(Repair.status == RepairStatus.PENDING)
    )
    
    return {
        "total_users": user_count.scalar() or 0,
        "total_properties": property_count.scalar() or 0,
        "total_communities": community_count.scalar() or 0,
        "unpaid_bills": unpaid_bills.scalar() or 0,
        "pending_repairs": pending_repairs.scalar() or 0,
    }
