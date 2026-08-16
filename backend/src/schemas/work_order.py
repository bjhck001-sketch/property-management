from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
import json
from src.models.work_order import WorkOrderType, WorkOrderStatus, Priority, InspectionTask


class WorkOrderCreate(BaseModel):
    property_id: int
    order_type: WorkOrderType
    title: str
    description: str
    priority: Priority = Priority.MEDIUM


class WorkOrderUpdate(BaseModel):
    status: Optional[WorkOrderStatus] = None
    assigned_to: Optional[int] = None
    photos: Optional[list] = None
    result: Optional[str] = None


class WorkOrderResponse(BaseModel):
    id: int
    property_id: int
    order_type: WorkOrderType
    title: str
    description: str
    priority: Priority
    assigned_to: Optional[int] = None
    status: WorkOrderStatus
    photos: list = []
    result: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('photos', mode='before')
    @classmethod
    def parse_photos(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v


class InspectionTaskCreate(BaseModel):
    property_id: int
    inspector_id: int
    task_name: str
    location: str


class InspectionTaskResponse(BaseModel):
    id: int
    property_id: int
    inspector_id: int
    task_name: str
    location: str
    status: WorkOrderStatus
    photos: list = []
    issue_description: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('photos', mode='before')
    @classmethod
    def parse_photos(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v
