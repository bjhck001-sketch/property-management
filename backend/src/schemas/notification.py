from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.models.notification import NotificationType


class NotificationCreate(BaseModel):
    target_user_id: int
    notification_type: NotificationType
    title: str
    content: str


class NotificationResponse(BaseModel):
    id: int
    target_user_id: int
    notification_type: NotificationType
    title: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
