import time
from typing import Any, Optional

class CacheService:
    """Simple in-memory cache service"""
    _cache = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in cls._cache:
            value, expiry = cls._cache[key]
            if expiry is None or time.time() < expiry:
                return value
            else:
                del cls._cache[key]
        return None
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with optional TTL"""
        expiry = time.time() + ttl if ttl else None
        cls._cache[key] = (value, expiry)
    
    @classmethod
    def delete(cls, key: str):
        """Delete value from cache"""
        if key in cls._cache:
            del cls._cache[key]
    
    @classmethod
    def clear(cls):
        """Clear all cache"""
        cls._cache.clear()
    
    @classmethod
    def size(cls) -> int:
        """Get cache size"""
        return len(cls._cache)