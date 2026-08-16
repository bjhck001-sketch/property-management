from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json
from src.database import get_db
from src.models.user import User
from src.models.notification import Notification, NotificationType
from src.models.community import Property
from src.schemas.notification import NotificationCreate, NotificationResponse
from src.middleware import get_current_user, require_role
from src.models.user import UserRole

router = APIRouter(tags=["Notifications"])


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's notifications"""
    result = await db.execute(
        select(Notification)
        .where(Notification.target_user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_create: NotificationCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Create a notification (admin only)"""
    db_notification = Notification(
        **notification_create.model_dump()
    )
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification


@router.post("/broadcast", response_model=List[NotificationResponse], status_code=status.HTTP_201_CREATED)
async def broadcast_notification(
    notification_create: NotificationCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """Broadcast notification to all users (admin only)"""
    from sqlalchemy import select as sa_select
    result = await db.execute(sa_select(User).where(User.status == True))
    users = result.scalars().all()
    
    created_notifications = []
    for user in users:
        notification = Notification(
            notification_type=notification_create.notification_type,
            title=notification_create.title,
            content=notification_create.content,
            target_user_id=user.id,
            priority=notification_create.priority,
            target_audience=notification_create.target_audience
        )
        db.add(notification)
        created_notifications.append(notification)
    
    await db.commit()
    for notification in created_notifications:
        await db.refresh(notification)
    
    return created_notifications


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark notification as read"""
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id)
        .where(Notification.target_user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    await db.commit()
    await db.refresh(notification)
    return notification


@router.post("/mark-all-read")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark all notifications as read"""
    await db.execute(
        Notification.__table__.update()
        .where(Notification.target_user_id == current_user.id)
        .where(Notification.is_read == False)
        .values(is_read=True)
    )
    await db.commit()
    return {"message": "All notifications marked as read"}
