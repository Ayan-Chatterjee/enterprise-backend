"""Callback repository implementation"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.callback import Callback
from src.domain.repositories.callback_repo import CallbackRepository
from src.infrastructure.database.models.callback_model import CallbackModel


class CallbackRepositoryImpl(CallbackRepository):
    """Implementation of CallbackRepository using SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, callback: Callback) -> Callback:
        """Create a new callback"""
        model = CallbackModel(
            contact_id=callback.contact_id,
            scheduled_at=callback.scheduled_at,
            status=callback.status,
            notes=callback.notes,
            assigned_to=callback.assigned_to,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)
    
    async def get_by_id(self, callback_id: int) -> Optional[Callback]:
        """Get callback by ID"""
        result = await self.session.execute(
            select(CallbackModel).where(CallbackModel.id == callback_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Callback]:
        """Get all callbacks with pagination"""
        result = await self.session.execute(
            select(CallbackModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def get_by_contact_id(self, contact_id: int) -> List[Callback]:
        """Get all callbacks for a contact"""
        result = await self.session.execute(
            select(CallbackModel).where(CallbackModel.contact_id == contact_id)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update(self, callback: Callback) -> Callback:
        """Update an existing callback"""
        model = await self.session.execute(
            select(CallbackModel).where(CallbackModel.id == callback.id)
        )
        existing = model.scalar_one()
        
        existing.scheduled_at = callback.scheduled_at
        existing.status = callback.status
        existing.notes = callback.notes
        existing.assigned_to = callback.assigned_to
        
        await self.session.flush()
        return self._to_entity(existing)
    
    async def delete(self, callback_id: int) -> bool:
        """Delete a callback"""
        result = await self.session.execute(
            select(CallbackModel).where(CallbackModel.id == callback_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
    
    @staticmethod
    def _to_entity(model: CallbackModel) -> Callback:
        """Convert model to entity"""
        return Callback(
            id=model.id,
            contact_id=model.contact_id,
            scheduled_at=model.scheduled_at,
            status=model.status,
            notes=model.notes,
            assigned_to=model.assigned_to,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
