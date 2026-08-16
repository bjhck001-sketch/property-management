from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PropertyBase(BaseModel):
    community_id: int
    owner_id: Optional[int] = None
    building_no: str
    unit_no: str = ""
    floor_no: str = ""
    room_no: str
    area: float = 0.0


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    building_no: Optional[str] = None
    unit_no: Optional[str] = None
    floor_no: Optional[str] = None
    room_no: Optional[str] = None
    area: Optional[float] = None


class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
