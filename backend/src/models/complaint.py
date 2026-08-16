from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class ComplaintType(str, enum.Enum):
    SERVICE = "service"
    FACILITY = "facility"
    NOISE = "noise"
    SANITATION = "sanitation"
    OTHER = "other"


class ComplaintStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CLOSED = "closed"


class Complaint(Base):
    __tablename__ = "complaints"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    submitter_id: Mapped[int] = mapped_column(index=True)
    complaint_type: Mapped[ComplaintType] = mapped_column(Enum(ComplaintType))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    images: Mapped[str] = mapped_column(Text, default="[]")
    status: Mapped[ComplaintStatus] = mapped_column(Enum(ComplaintStatus), default=ComplaintStatus.PENDING)
    response: Mapped[str] = mapped_column(Text, default="")
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Complaint(id={self.id}, status={self.status})>"
