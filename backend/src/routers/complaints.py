from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json
from src.database import get_db
from src.models.user import User
from src.models.complaint import Complaint, ComplaintType, ComplaintStatus
from src.models.community import Property
from src.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole
from datetime import datetime

router = APIRouter(tags=["Complaints"])


@router.get("/", response_model=List[ComplaintResponse])
async def list_complaints(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List complaints"""
    query = select(Complaint)
    
    if current_user.role != UserRole.ADMIN:
        query = query.where(Complaint.submitter_id == current_user.id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_create: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new complaint"""
    # Verify property belongs to user
    prop_result = await db.execute(
        select(Property).where(Property.id == complaint_create.property_id)
    )
    property = prop_result.scalar_one_or_none()
    if not property or property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    db_complaint = Complaint(
        **complaint_create.model_dump(),
        submitter_id=current_user.id
    )
    db_complaint.images = json.dumps(complaint_create.images) if isinstance(complaint_create.images, list) else complaint_create.images
    db.add(db_complaint)
    await db.commit()
    await db.refresh(db_complaint)
    return db_complaint


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get complaint details"""
    result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    if complaint.submitter_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update complaint status"""
    result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    for field, value in complaint_update.model_dump(exclude_unset=True).items():
        setattr(complaint, field, value)
    
    if complaint.status == ComplaintStatus.COMPLETED and not complaint.completed_at:
        complaint.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(complaint)
    return complaint
