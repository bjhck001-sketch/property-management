from datetime import datetime
from sqlalchemy import String, DateTime, Numeric, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
import enum


class PaymentMethod(str, enum.Enum):
    WECHAT = "wechat"
    ALIPAY = "alipay"
    OTHER = "other"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bill_id: Mapped[int] = mapped_column(index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), default=PaymentMethod.WECHAT)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id: Mapped[str] = mapped_column(String(100), default="")
    paid_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"
