import redis

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

def ping_redis():
    try:
        redis_client.ping()
        return True
    except Exception:
        return False