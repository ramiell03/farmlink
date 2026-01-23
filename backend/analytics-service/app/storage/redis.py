import redis
from app.core.config import settings

redis_client = None

def get_redis():
    global redis_client

    if redis_client is None:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
            )

    return redis_client
