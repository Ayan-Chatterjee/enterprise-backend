"""Contact DTOs"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactCreateDTO(BaseModel):
    """DTO for creating a contact"""
    
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(default="", max_length=1000)
    source: Optional[str] = Field(None, max_length=100)


class ContactUpdateDTO(BaseModel):
    """DTO for updating a contact"""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    message: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None


class ContactResponseDTO(BaseModel):
    """DTO for contact responses"""
    
    id: int
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    message: str
    status: str
    source: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config"""
        from_attributes = True
