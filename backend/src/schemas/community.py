from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommunityBase(BaseModel):
    name: str
    address: Optional[str] = None
    contact_phone: Optional[str] = None


class CommunityCreate(CommunityBase):
    pass


class CommunityUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None


class CommunityResponse(CommunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PropertyBase(BaseModel):
    community_id: int
    owner_id: Optional[int] = None
    building_no: str
    unit_no: Optional[str] = None
    floor_no: str
    room_no: str
    area: Optional[float] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    community_id: Optional[int] = None
    owner_id: Optional[int] = None
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
