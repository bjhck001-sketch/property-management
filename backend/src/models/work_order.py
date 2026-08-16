from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class WorkOrderType(str, enum.Enum):
    REPAIR = "repair"
    INSPECTION = "inspection"
    OTHER = "other"


class WorkOrderStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class WorkOrder(Base):
    __tablename__ = "work_orders"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    order_type: Mapped[WorkOrderType] = mapped_column(Enum(WorkOrderType))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.MEDIUM)
    assigned_to: Mapped[int] = mapped_column(default=None, nullable=True)
    status: Mapped[WorkOrderStatus] = mapped_column(Enum(WorkOrderStatus), default=WorkOrderStatus.PENDING)
    photos: Mapped[str] = mapped_column(Text, default="[]")
    result: Mapped[str] = mapped_column(Text, default="")
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<WorkOrder(id={self.id}, status={self.status})>"


class InspectionTask(Base):
    __tablename__ = "inspection_tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    inspector_id: Mapped[int] = mapped_column(index=True)
    task_name: Mapped[str] = mapped_column(String(200))
    location: Mapped[str] = mapped_column(String(500))
    status: Mapped[WorkOrderStatus] = mapped_column(Enum(WorkOrderStatus), default=WorkOrderStatus.PENDING)
    photos: Mapped[str] = mapped_column(Text, default="[]")
    issue_description: Mapped[str] = mapped_column(Text, default="")
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<InspectionTask(id={self.id}, status={self.status})>"
