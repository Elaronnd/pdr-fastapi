from typing import Any, Optional
from aiocache import caches


async def delete_cache(key: str, cache_id: int):
    cache = caches.get("default")
    await cache.delete(f"{key}:{cache_id}")


async def set_cache(key: str, value: Any, cache_id: Optional[int] = None, ttl: int = 60):
    cache = caches.get("default")
    full_key = f"{key}:{cache_id}" if cache_id is not None else key
    await cache.set(full_key, value, ttl=ttl)
