"""Callback DTOs"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CallbackCreateDTO(BaseModel):
    """DTO for creating a callback"""
    
    contact_id: int = Field(..., gt=0)
    scheduled_at: Optional[datetime] = None
    notes: str = Field(default="", max_length=500)
    assigned_to: Optional[int] = None


class CallbackUpdateDTO(BaseModel):
    """DTO for updating a callback"""
    
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    assigned_to: Optional[int] = None


class CallbackResponseDTO(BaseModel):
    """DTO for callback responses"""
    
    id: int
    contact_id: int
    scheduled_at: Optional[datetime]
    status: str
    notes: str
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config"""
        from_attributes = True
