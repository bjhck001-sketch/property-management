from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class NotificationType(str, enum.Enum):
    REPAIR = "repair"
    BILL = "bill"
    ANNOUNCEMENT = "announcement"
    ACTIVITY = "activity"
    SYSTEM = "system"


class Notification(Base):
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    target_user_id: Mapped[int] = mapped_column(index=True)
    notification_type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.notification_type})>"
