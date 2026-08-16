from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.models.bill import BillType, BillStatus


class BillBase(BaseModel):
    property_id: int
    bill_type: BillType
    amount: float
    period: str
    due_date: datetime


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    status: Optional[BillStatus] = None


class BillResponse(BillBase):
    id: int
    status: BillStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
