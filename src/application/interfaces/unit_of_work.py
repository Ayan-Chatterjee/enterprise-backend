"""Unit of Work interface for transaction management"""
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.repositories.contact_repo import ContactRepository
from src.domain.repositories.callback_repo import CallbackRepository
from src.domain.repositories.user_repo import UserRepository


class UnitOfWork(ABC):
    """Unit of Work interface for managing transactions"""
    
    contacts: ContactRepository
    callbacks: CallbackRepository
    users: UserRepository
    
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        """Context manager entry"""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit"""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit the transaction"""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction"""
        pass
