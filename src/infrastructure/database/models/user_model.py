"""User database model"""
from sqlalchemy import Column, String, Boolean, Index
from src.infrastructure.database.base import BaseModel


class UserModel(BaseModel):
    """User database model"""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    __table_args__ = (
        Index("idx_email_active", "email", "is_active"),
    )
