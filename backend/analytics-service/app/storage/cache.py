import json
from typing import Any, Optional
from app.storage.redis import get_redis

DEFAULT_TTL = 300  

def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL):
    redis = get_redis()
    redis.setex(key, ttl, json.dumps(value))


def cache_get(key: str) -> Optional[Any]:
    redis = get_redis()
    value = redis.get(key)
    return json.loads(value) if value else None


def cache_delete(key: str):
    redis = get_redis()
    redis.delete(key)
    

