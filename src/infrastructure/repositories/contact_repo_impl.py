"""Contact repository implementation"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.contact import Contact
from src.domain.repositories.contact_repo import ContactRepository
from src.infrastructure.database.models.contact_model import ContactModel


class ContactRepositoryImpl(ContactRepository):
    """Implementation of ContactRepository using SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, contact: Contact) -> Contact:
        """Create a new contact"""
        model = ContactModel(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            message=contact.message,
            status=contact.status,
            source=contact.source,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)
    
    async def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID"""
        result = await self.session.execute(
            select(ContactModel).where(ContactModel.id == contact_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Contact]:
        """Get all contacts with pagination"""
        result = await self.session.execute(
            select(ContactModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update(self, contact: Contact) -> Contact:
        """Update an existing contact"""
        model = await self.session.execute(
            select(ContactModel).where(ContactModel.id == contact.id)
        )
        existing = model.scalar_one()
        
        existing.first_name = contact.first_name
        existing.last_name = contact.last_name
        existing.email = contact.email
        existing.phone = contact.phone
        existing.message = contact.message
        existing.status = contact.status
        existing.source = contact.source
        
        await self.session.flush()
        return self._to_entity(existing)
    
    async def delete(self, contact_id: int) -> bool:
        """Delete a contact"""
        result = await self.session.execute(
            select(ContactModel).where(ContactModel.id == contact_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
    
    async def find_by_email(self, email: str) -> Optional[Contact]:
        """Find contact by email"""
        result = await self.session.execute(
            select(ContactModel).where(ContactModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    @staticmethod
    def _to_entity(model: ContactModel) -> Contact:
        """Convert model to entity"""
        return Contact(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone=model.phone,
            message=model.message,
            status=model.status,
            source=model.source,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
