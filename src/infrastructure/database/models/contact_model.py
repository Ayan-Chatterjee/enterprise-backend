"""Contact database model"""
from sqlalchemy import Column, String, Text, Index
from src.infrastructure.database.base import BaseModel


class ContactModel(BaseModel):
    """Contact database model"""
    
    __tablename__ = "contacts"
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), index=True, nullable=True)
    phone = Column(String(20), index=True, nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String(50), default="new", nullable=False, index=True)
    source = Column(String(100), nullable=True)
    
    __table_args__ = (
        Index("idx_email_phone", "email", "phone"),
        Index("idx_status_created", "status", "created_at"),
    )
