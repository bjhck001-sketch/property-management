from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json
from src.database import get_db
from src.models.user import User
from src.models.repair import Repair, RepairType, RepairStatus
from src.models.community import Property
from src.schemas.repair import RepairCreate, RepairUpdate, RepairResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Repairs"])


@router.get("/", response_model=List[RepairResponse])
async def list_repairs(
    skip: int = 0,
    limit: int = 100,
    status_filter: RepairStatus = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List repairs"""
    query = select(Repair)
    
    if status_filter:
        query = query.where(Repair.status == status_filter)
    
    if current_user.role != UserRole.ADMIN:
        query = query.where(Repair.submitter_id == current_user.id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=RepairResponse, status_code=status.HTTP_201_CREATED)
async def create_repair(
    repair_create: RepairCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new repair request"""
    # Verify property belongs to user
    prop_result = await db.execute(
        select(Property).where(Property.id == repair_create.property_id)
    )
    property = prop_result.scalar_one_or_none()
    if not property or property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    repair_data = repair_create.model_dump()
    repair_data.pop('images', None)  # Remove images to handle separately
    repair_data['images'] = json.dumps(repair_create.images) if isinstance(repair_create.images, list) else repair_create.images
    repair_data['submitter_id'] = current_user.id
    db_repair = Repair(**repair_data)
    db.add(db_repair)
    await db.commit()
    await db.refresh(db_repair)
    return db_repair


@router.get("/{repair_id}", response_model=RepairResponse)
async def get_repair(
    repair_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get repair details"""
    result = await db.execute(select(Repair).where(Repair.id == repair_id))
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    if repair.submitter_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    return repair


@router.put("/{repair_id}", response_model=RepairResponse)
async def update_repair(
    repair_id: int,
    repair_update: RepairUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update repair status"""
    result = await db.execute(select(Repair).where(Repair.id == repair_id))
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    # Only admin or assigned staff can update
    if current_user.role != UserRole.ADMIN and repair.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    for field, value in repair_update.model_dump(exclude_unset=True).items():
        setattr(repair, field, value)
    
    if repair.status == RepairStatus.COMPLETED and not repair.completed_at:
        from datetime import datetime
        repair.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/evaluate", response_model=RepairResponse)
async def evaluate_repair(
    repair_id: int,
    rating: int,
    comment: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Rate a completed repair"""
    result = await db.execute(select(Repair).where(Repair.id == repair_id))
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    if repair.submitter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    if repair.status != RepairStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Can only rate completed repairs")
    
    repair.rating = rating
    repair.comment = comment
    await db.commit()
    await db.refresh(repair)
    return repair
