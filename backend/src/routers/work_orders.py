from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import json
from src.database import get_db
from src.models.user import User
from src.models.work_order import WorkOrder, WorkOrderType, WorkOrderStatus, Priority, InspectionTask
from src.models.community import Property
from src.schemas.work_order import (
    WorkOrderCreate, WorkOrderUpdate, WorkOrderResponse,
    InspectionTaskCreate, InspectionTaskResponse
)
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Work Orders"])


# Work Orders
@router.get("/work-orders/", response_model=List[WorkOrderResponse])
async def list_work_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: WorkOrderStatus = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List work orders"""
    query = select(WorkOrder)
    
    if status_filter:
        query = query.where(WorkOrder.status == status_filter)
    
    if current_user.role == UserRole.STAFF:
        query = query.where(WorkOrder.assigned_to == current_user.id)
    elif current_user.role != UserRole.ADMIN:
        query = query.where(WorkOrder.property_id.in_(
            select(Property.id).where(Property.owner_id == current_user.id)
        ))
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/work-orders/", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_work_order(
    order_create: WorkOrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new work order"""
    db_order = WorkOrder(**order_create.model_dump())
    db_order.photos = json.dumps(order_create.photos) if getattr(order_create, 'photos', None) else '[]'
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


@router.put("/work-orders/{order_id}", response_model=WorkOrderResponse)
async def update_work_order(
    order_id: int,
    order_update: WorkOrderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update work order"""
    result = await db.execute(select(WorkOrder).where(WorkOrder.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    if current_user.role != UserRole.ADMIN and order.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    for field, value in order_update.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    
    if order.status == WorkOrderStatus.COMPLETED and not order.completed_at:
        from datetime import datetime
        order.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(order)
    return order


# Inspection Tasks
@router.get("/inspection-tasks/", response_model=List[InspectionTaskResponse])
async def list_inspection_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List inspection tasks"""
    query = select(InspectionTask)
    
    if current_user.role == UserRole.STAFF:
        query = query.where(InspectionTask.inspector_id == current_user.id)
    elif current_user.role != UserRole.ADMIN:
        query = query.where(InspectionTask.property_id.in_(
            select(Property.id).where(Property.owner_id == current_user.id)
        ))
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/inspection-tasks/", response_model=InspectionTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_inspection_task(
    task_create: InspectionTaskCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Create an inspection task (admin only)"""
    db_task = InspectionTask(**task_create.model_dump())
    db_task.photos = json.dumps(task_create.photos) if getattr(task_create, 'photos', None) else '[]'
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


# Stats
@router.get("/stats/", response_model=dict)
async def get_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Get statistics (admin only)"""
    # Today's repair count
    repair_count = await db.execute(
        select(func.count()).where(WorkOrder.order_type == WorkOrderType.REPAIR)
    )
    # Pending work orders
    pending_count = await db.execute(
        select(func.count()).where(WorkOrder.status == WorkOrderStatus.PENDING)
    )
    # Overdue bills
    from src.models.bill import Bill, BillStatus
    from datetime import datetime
    overdue_count = await db.execute(
        select(func.count()).where(
            Bill.status == BillStatus.PENDING,
            Bill.due_date < datetime.utcnow()
        )
    )
    
    return {
        "today_repairs": repair_count.scalar() or 0,
        "pending_orders": pending_count.scalar() or 0,
        "overdue_bills": overdue_count.scalar() or 0,
    }
