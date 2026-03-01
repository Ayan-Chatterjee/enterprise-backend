"""Database session management"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import get_settings

settings = get_settings()


def get_async_engine():
    """Create async SQLAlchemy engine"""
    return create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        future=True,
    )


async def get_async_session_maker():
    """Get async session maker"""
    engine = get_async_engine()
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_session():
    """Dependency for getting DB session"""
    session_maker = await get_async_session_maker()
    async with session_maker() as session:
        yield session
