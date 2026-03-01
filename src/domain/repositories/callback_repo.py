"""Repository interfaces for Callback entity"""
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.callback import Callback


class CallbackRepository(ABC):
    """Abstract repository interface for Callback entity"""
    
    @abstractmethod
    async def create(self, callback: Callback) -> Callback:
        """Create a new callback"""
        pass
    
    @abstractmethod
    async def get_by_id(self, callback_id: int) -> Optional[Callback]:
        """Get callback by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Callback]:
        """Get all callbacks with pagination"""
        pass
    
    @abstractmethod
    async def get_by_contact_id(self, contact_id: int) -> List[Callback]:
        """Get all callbacks for a contact"""
        pass
    
    @abstractmethod
    async def update(self, callback: Callback) -> Callback:
        """Update an existing callback"""
        pass
    
    @abstractmethod
    async def delete(self, callback_id: int) -> bool:
        """Delete a callback"""
        pass
