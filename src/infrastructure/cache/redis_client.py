"""Redis client for caching"""
from typing import Any, Optional
import json
import redis.asyncio as redis
from src.core.config import get_settings

settings = get_settings()


class RedisClient:
    """Redis client wrapper for async operations"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis"""
        if settings.redis_enabled and settings.redis_url:
            self.client = await redis.from_url(settings.redis_url, decode_responses=True)
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache"""
        if not self.client:
            return False
        try:
            serialized = json.dumps(value) if not isinstance(value, str) else value
            await self.client.setex(key, ttl, serialized)
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.client:
            return False
        await self.client.delete(key)
        return True
    
    async def clear(self) -> bool:
        """Clear all cache"""
        if not self.client:
            return False
        await self.client.flushdb()
        return True


redis_client = RedisClient()
