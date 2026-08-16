from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.models.payment import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    bill_id: int
    payment_method: PaymentMethod = PaymentMethod.WECHAT


class PaymentResponse(BaseModel):
    id: int
    bill_id: int
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
