"""User entity"""
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """User entity representing a system user"""
    
    id: Optional[int] = None
    email: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate user entity"""
        if not self.email:
            raise ValueError("Email is required")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
    
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
