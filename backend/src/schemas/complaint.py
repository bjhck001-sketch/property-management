from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
import json
from src.models.complaint import ComplaintType, ComplaintStatus


class ComplaintCreate(BaseModel):
    property_id: int
    complaint_type: ComplaintType
    title: str
    description: str
    images: list = []


class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    response: Optional[str] = None


class ComplaintResponse(BaseModel):
    id: int
    property_id: int
    submitter_id: int
    complaint_type: ComplaintType
    title: str
    description: str
    images: list = []
    status: ComplaintStatus
    response: str
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
