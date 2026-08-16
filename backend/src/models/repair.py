from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class RepairType(str, enum.Enum):
    INDOOR = "indoor"
    PUBLIC = "public"


class RepairStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Repair(Base):
    __tablename__ = "repairs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    submitter_id: Mapped[int] = mapped_column(index=True)
    repair_type: Mapped[RepairType] = mapped_column(Enum(RepairType))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    images: Mapped[str] = mapped_column(Text, default="[]")  # JSON array of image URLs
    assigned_to: Mapped[int] = mapped_column(default=None, nullable=True)
    status: Mapped[RepairStatus] = mapped_column(Enum(RepairStatus), default=RepairStatus.PENDING)
    rating: Mapped[int] = mapped_column(default=0)  # 1-5
    comment: Mapped[str] = mapped_column(Text, default="")
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Repair(id={self.id}, status={self.status})>"
