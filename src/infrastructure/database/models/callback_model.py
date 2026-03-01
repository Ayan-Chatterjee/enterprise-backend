"""Callback database model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from src.infrastructure.database.base import BaseModel


class CallbackModel(BaseModel):
    """Callback database model"""
    
    __tablename__ = "callbacks"
    
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True)
    status = Column(String(50), default="pending", nullable=False, index=True)
    notes = Column(Text, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    __table_args__ = (
        Index("idx_contact_status", "contact_id", "status"),
        Index("idx_scheduled_status", "scheduled_at", "status"),
    )
