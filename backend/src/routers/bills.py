from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.database import get_db
from src.models.user import User
from src.models.bill import Bill, BillType, BillStatus
from src.models.community import Property
from src.schemas.bill import BillCreate, BillUpdate, BillResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole
from datetime import datetime

router = APIRouter(tags=["Bills"])


@router.get("/", response_model=List[BillResponse])
async def list_bills(
    skip: int = 0,
    limit: int = 100,
    property_id: int = None,
    status_filter: BillStatus = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List bills"""
    query = select(Bill)
    
    if property_id:
        query = query.where(Bill.property_id == property_id)
    if status_filter:
        query = query.where(Bill.status == status_filter)
    if current_user.role != UserRole.ADMIN:
        # Non-admin users can only see their own properties' bills
        properties = await db.execute(
            select(Property.id).where(Property.owner_id == current_user.id)
        )
        property_ids = [p.id for p in properties.scalars().all()]
        if property_ids:
            query = query.where(Bill.property_id.in_(property_ids))
        else:
            query = query.where(Bill.property_id == -1)  # No results
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(
    bill_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get bill details"""
    result = await db.execute(select(Bill).where(Bill.id == bill_id))
    bill = result.scalar_one_or_none()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(
    bill_create: BillCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Create a new bill (admin only)"""
    db_bill = Bill(**bill_create.model_dump())
    db.add(db_bill)
    await db.commit()
    await db.refresh(db_bill)
    return db_bill


@router.post("/batch-generate", response_model=List[BillResponse])
async def batch_generate_bills(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Batch generate bills for all properties (admin only)"""
    # Get all properties
    result = await db.execute(select(Property))
    properties = result.scalars().all()
    
    generated_bills = []
    for property in properties:
        # Generate a property fee bill for current month
        bill = Bill(
            property_id=property.id,
            bill_type=BillType.PROPERTY_FEE,
            amount=property.area * 2.5,  # Example: 2.5 per sq meter
            period=datetime.utcnow().strftime("%Y-%m"),
            status=BillStatus.PENDING,
            due_date=datetime.utcnow().replace(day=28)  # Due on 28th of month
        )
        db.add(bill)
        generated_bills.append(bill)
    
    await db.commit()
    for bill in generated_bills:
        await db.refresh(bill)
    
    return generated_bills


@router.put("/{bill_id}", response_model=BillResponse)
async def update_bill(
    bill_id: int,
    bill_update: BillUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Update bill (admin only)"""
    result = await db.execute(select(Bill).where(Bill.id == bill_id))
    bill = result.scalar_one_or_none()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    for field, value in bill_update.model_dump(exclude_unset=True).items():
        setattr(bill, field, value)
    
    await db.commit()
    await db.refresh(bill)
    return bill
