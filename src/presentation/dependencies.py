"""Dependency injection container for FastAPI"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.contact_repo_impl import ContactRepositoryImpl
from src.infrastructure.repositories.callback_repo_impl import CallbackRepositoryImpl
from src.infrastructure.repositories.user_repo_impl import UserRepositoryImpl


def get_contact_repository(session: AsyncSession = Depends(get_session)) -> ContactRepositoryImpl:
    """Get contact repository instance"""
    return ContactRepositoryImpl(session)


def get_callback_repository(session: AsyncSession = Depends(get_session)) -> CallbackRepositoryImpl:
    """Get callback repository instance"""
    return CallbackRepositoryImpl(session)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    """Get user repository instance"""
    return UserRepositoryImpl(session)
