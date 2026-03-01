"""Repository interfaces - defining contracts for data access"""
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.contact import Contact


class ContactRepository(ABC):
    """Abstract repository interface for Contact entity"""
    
    @abstractmethod
    async def create(self, contact: Contact) -> Contact:
        """Create a new contact"""
        pass
    
    @abstractmethod
    async def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Contact]:
        """Get all contacts with pagination"""
        pass
    
    @abstractmethod
    async def update(self, contact: Contact) -> Contact:
        """Update an existing contact"""
        pass
    
    @abstractmethod
    async def delete(self, contact_id: int) -> bool:
        """Delete a contact"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Contact]:
        """Find contact by email"""
        pass
