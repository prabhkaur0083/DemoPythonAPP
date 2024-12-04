import redis
from datetime import timedelta

# Initialize Redis client
redisClient = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
