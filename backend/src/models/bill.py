from datetime import datetime
from sqlalchemy import String, DateTime, Numeric, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class BillType(str, enum.Enum):
    PROPERTY_FEE = "property_fee"
    UTILITY_FEE = "utility_fee"
    PARKING_FEE = "parking_fee"
    OTHER = "other"


class BillStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Bill(Base):
    __tablename__ = "bills"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(index=True)
    bill_type: Mapped[BillType] = mapped_column(Enum(BillType))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    period: Mapped[str] = mapped_column(String(20))  # e.g., "2024-01"
    status: Mapped[BillStatus] = mapped_column(Enum(BillStatus), default=BillStatus.PENDING)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Bill(id={self.id}, type={self.bill_type}, amount={self.amount})>"
