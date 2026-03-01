"""User repository implementation"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.domain.repositories.user_repo import UserRepository
from src.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """Implementation of UserRepository using SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user"""
        model = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_admin=user.is_admin,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def update(self, user: User) -> User:
        """Update an existing user"""
        model = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        existing = model.scalar_one()
        
        existing.email = user.email
        existing.password_hash = user.password_hash
        existing.first_name = user.first_name
        existing.last_name = user.last_name
        existing.is_active = user.is_active
        existing.is_admin = user.is_admin
        
        await self.session.flush()
        return self._to_entity(existing)
    
    async def delete(self, user_id: int) -> bool:
        """Delete a user"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convert model to entity"""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            is_admin=model.is_admin,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
