"""Callback entity"""
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Callback:
    """Callback entity representing a scheduled callback request"""
    
    id: Optional[int] = None
    contact_id: int = 0
    scheduled_at: Optional[datetime] = None
    status: str = "pending"
    notes: str = ""
    assigned_to: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate callback entity"""
        if self.contact_id <= 0:
            raise ValueError("Contact ID is required")
        if self.scheduled_at and self.scheduled_at < datetime.utcnow():
            raise ValueError("Scheduled time cannot be in the past")
