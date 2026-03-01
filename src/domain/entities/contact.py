"""Contact entity"""
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Contact:
    """Contact entity representing a prospective customer"""
    
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    message: str = ""
    status: str = "new"
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate contact entity"""
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        if not self.email and not self.phone:
            raise ValueError("At least email or phone is required")
    
    def full_name(self) -> str:
        """Get contact's full name"""
        return f"{self.first_name} {self.last_name}".strip()
