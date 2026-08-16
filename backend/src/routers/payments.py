from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from src.database import get_db
from src.models.user import User
from src.models.payment import Payment, PaymentMethod, PaymentStatus
from src.models.bill import Bill, BillStatus
from src.schemas.payment import PaymentCreate, PaymentResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Payments"])


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List payments"""
    # Admin can see all payments, others see their own bills' payments
    if current_user.role == UserRole.ADMIN:
        query = select(Payment).offset(skip).limit(limit)
    else:
        # Get user's properties
        from src.models.community import Property
        result = await db.execute(
            select(Property.id).where(Property.owner_id == current_user.id)
        )
        property_ids = result.scalars().all()
        
        # Get bills for these properties
        bill_result = await db.execute(
            select(Bill.id).where(Bill.property_id.in_(property_ids))
        )
        bill_ids = [b.id for b in bill_result.scalars().all()]
        
        query = select(Payment).where(Payment.bill_id.in_(bill_ids)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/create", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_create: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a payment order"""
    # Check if bill exists and belongs to user
    result = await db.execute(select(Bill).where(Bill.id == payment_create.bill_id))
    bill = result.scalar_one_or_none()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    if current_user.role != UserRole.ADMIN:
        prop_result = await db.execute(
            select(Property).where(Property.id == bill.property_id)
        )
        property = prop_result.scalar_one_or_none()
        if not property or property.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
    
    # Check if bill is already paid
    if bill.status == BillStatus.PAID:
        raise HTTPException(status_code=400, detail="Bill is already paid")
    
    # Create payment
    payment = Payment(
        bill_id=payment_create.bill_id,
        amount=float(bill.amount),
        payment_method=payment_create.payment_method,
        status=PaymentStatus.PENDING
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Confirm payment (mock payment)"""
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Update payment status
    payment.status = PaymentStatus.COMPLETED
    payment.paid_at = datetime.utcnow()
    payment.transaction_id = f"MOCK_{payment_id}_{int(time.time())}"
    
    # Update bill status
    bill_result = await db.execute(select(Bill).where(Bill.id == payment.bill_id))
    bill = bill_result.scalar_one_or_none()
    if bill:
        bill.status = BillStatus.PAID
    
    await db.commit()
    await db.refresh(payment)
    return payment


import time
from datetime import datetime
from src.models.community import Property
