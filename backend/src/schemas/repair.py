from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
import json
from src.models.repair import RepairType, RepairStatus


class RepairCreate(BaseModel):
    property_id: int
    repair_type: RepairType
    title: str
    description: str
    images: list = []


class RepairUpdate(BaseModel):
    status: Optional[RepairStatus] = None
    assigned_to: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None


class RepairResponse(BaseModel):
    id: int
    property_id: int
    submitter_id: int
    repair_type: RepairType
    title: str
    description: str
    images: list = []
    assigned_to: Optional[int] = None
    status: RepairStatus
    rating: int
    comment: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('images', mode='before')
    @classmethod
    def parse_images(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v
