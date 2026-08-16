from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import secrets
from src.database import get_db
from src.models.user import User
from src.models.visitor import Visitor, VisitorStatus
from src.models.community import Property
from src.schemas.visitor import VisitorCreate, VisitorResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole
from datetime import datetime, timedelta

router = APIRouter(tags=["Visitors"])


@router.get("/", response_model=List[VisitorResponse])
async def list_visitors(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List visitors"""
    query = select(Visitor)
    
    if current_user.role != UserRole.ADMIN:
        query = query.where(Visitor.submitter_id == current_user.id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=VisitorResponse, status_code=status.HTTP_201_CREATED)
async def create_visitor(
    visitor_create: VisitorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a visitor record"""
    # Verify property belongs to user
    prop_result = await db.execute(
        select(Property).where(Property.id == visitor_create.property_id)
    )
    property = prop_result.scalar_one_or_none()
    if not property or property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    # Generate access code
    access_code = secrets.token_hex(4)
    
    db_visitor = Visitor(
        **visitor_create.model_dump(),
        submitter_id=current_user.id,
        access_code=access_code
    )
    db.add(db_visitor)
    await db.commit()
    await db.refresh(db_visitor)
    return db_visitor


@router.get("/{visitor_id}", response_model=VisitorResponse)
async def get_visitor(
    visitor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get visitor details"""
    result = await db.execute(select(Visitor).where(Visitor.id == visitor_id))
    visitor = result.scalar_one_or_none()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    if visitor.submitter_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    return visitor


@router.post("/{visitor_id}/check-in", response_model=VisitorResponse)
async def check_in_visitor(
    visitor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check in visitor"""
    result = await db.execute(select(Visitor).where(Visitor.id == visitor_id))
    visitor = result.scalar_one_or_none()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    if visitor.status != VisitorStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Visitor not approved")
    
    visitor.status = VisitorStatus.CHECKED_IN
    visitor.check_in_time = datetime.utcnow()
    await db.commit()
    await db.refresh(visitor)
    return visitor
