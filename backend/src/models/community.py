from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Community(Base):
    __tablename__ = "communities"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(String(500))
    contact_phone: Mapped[str] = mapped_column(String(20), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Community(id={self.id}, name={self.name})>"


class Property(Base):
    __tablename__ = "properties"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    community_id: Mapped[int] = mapped_column(index=True)
    owner_id: Mapped[int] = mapped_column(index=True)
    building_no: Mapped[str] = mapped_column(String(20))
    unit_no: Mapped[str] = mapped_column(String(20), default="")
    floor_no: Mapped[str] = mapped_column(String(20), default="")
    room_no: Mapped[str] = mapped_column(String(20))
    area: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Property(id={self.id}, room={self.room_no})>"
