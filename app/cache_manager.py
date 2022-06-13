import redis

r = redis.Redis(host='localhost', port=6379)

def check(key) -> bool:
    return r.exists(key)

def set(key, value):
    r.setex(key, 172800, value)

def get(key):
    return r.get(key)
