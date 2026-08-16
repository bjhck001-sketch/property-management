from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.database import get_db
from src.models.user import User
from src.models.community import Property
from src.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Properties"])


@router.get("/", response_model=List[PropertyResponse])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's properties"""
    result = await db.execute(
        select(Property).where(Property.owner_id == current_user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_create: PropertyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new property"""
    property_create.owner_id = current_user.id
    db_property = Property(**property_create.model_dump())
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return db_property


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get property details"""
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property = result.scalar_one_or_none()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    # Check ownership
    if property.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    return property


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_update: PropertyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update property"""
    result = await db.execute(select(Property).where(Property.id == property_id))
    property = result.scalar_one_or_none()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if property.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    for field, value in property_update.model_dump(exclude_unset=True).items():
        setattr(property, field, value)
    
    await db.commit()
    await db.refresh(property)
    return property


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete property"""
    result = await db.execute(select(Property).where(Property.id == property_id))
    property = result.scalar_one_or_none()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if property.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    await db.delete(property)
    await db.commit()
    return None
