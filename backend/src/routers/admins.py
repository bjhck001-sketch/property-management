from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.database import get_db
from src.models.user import User
from src.models.community import Community, Property
from src.models.bill import Bill
from src.models.repair import Repair
from src.schemas.user import UserResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Admin"])


@router.get("/users/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """List all users (admin only)"""
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/properties/", response_model=List)
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


@router.get("/communities/", response_model=List)
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


@router.get("/stats/", response_model=dict)
async def get_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Get system statistics (admin only)"""
    from sqlalchemy import func
    from src.models.bill import BillStatus
    from src.models.repair import RepairStatus
    from datetime import datetime
    
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
