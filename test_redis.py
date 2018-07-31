import redis

r = redis.Redis.from_url('redis://localhost:6379', db=1)
for key in r.scan_iter("*"):
    print("key:", key)
    r.delete(key)