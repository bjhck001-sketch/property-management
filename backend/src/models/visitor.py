from datetime import datetime
from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class VisitorStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"


class Visitor(Base):
    __tablename__ = "visitors"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    submitter_id: Mapped[int] = mapped_column(index=True)
    visitor_name: Mapped[str] = mapped_column(String(100))
    visitor_phone: Mapped[str] = mapped_column(String(20))
    access_code: Mapped[str] = mapped_column(String(50))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[VisitorStatus] = mapped_column(Enum(VisitorStatus), default=VisitorStatus.PENDING)
    check_in_time: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    check_out_time: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Visitor(id={self.id}, visitor={self.visitor_name})>"
