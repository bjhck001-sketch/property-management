from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.models.visitor import VisitorStatus


class VisitorCreate(BaseModel):
    property_id: int
    visitor_name: str
    visitor_phone: str
    start_time: datetime
    end_time: datetime


class VisitorResponse(BaseModel):
    id: int
    property_id: int
    submitter_id: int
    visitor_name: str
    visitor_phone: str
    access_code: str
    start_time: datetime
    end_time: datetime
    status: VisitorStatus
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
