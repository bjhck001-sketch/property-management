from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.models.user import UserRole


class UserBase(BaseModel):
    phone: str
    role: UserRole = UserRole.OWNER
    name: str = ""


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    phone: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    id: int
    status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
