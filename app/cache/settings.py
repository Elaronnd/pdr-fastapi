from aiocache import caches
from app.config.config import (
    REDIS_PORT,
    REDIS_ADDRESS
)

async def set_redis():
    caches.set_config({
        "default": {
            "cache": "aiocache.RedisCache",
            "endpoint": REDIS_ADDRESS,
            "port": REDIS_PORT,
            "serializer": {
                "class": "aiocache.serializers.JsonSerializer"
            }
        }
    })
