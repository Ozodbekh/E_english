import redis

r = redis.Redis()
r.mset({"code": 123456})
r.expire("code", 5)
print(r.mget("code")[0].decode())