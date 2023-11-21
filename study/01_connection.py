import redis
import sys

from decouple import config


REDISOLAR_REDIS_DB_LINK = config("REDISOLAR_REDIS_DB_LINK")
REDISOLAR_REDIS_DB_PORT = config("REDISOLAR_REDIS_DB_PORT", cast=int)
REDISOLAR_REDIS_USERNAME = config("REDISOLAR_REDIS_USERNAME")
REDISOLAR_REDIS_PASSWORD = config("REDISOLAR_REDIS_PASSWORD")


client = redis.Redis(host=REDISOLAR_REDIS_DB_LINK, port=REDISOLAR_REDIS_DB_PORT,
                     username=REDISOLAR_REDIS_USERNAME, password=REDISOLAR_REDIS_PASSWORD,
                     decode_responses=True)


print("Hello World")
result = client.set("hello", "world")
print(result)
val = client.get("hello")
print(val)
client.delete("hello")
print(80*"-")


print("list")
result = client.rpush("hello", *["a", "b", "a", "c"])
print(result)
vals = client.lrange("hello", 0, -1)
print(vals)
client.delete("hello")
print(80*"-")


print("set")
result = client.sadd("hello", *["a", "b", "a", "c"])
print(result)
vals = client.smembers("hello")
print(vals)
client.delete("hello")
print(80*"-")


print("dictionary")
result = client.hset("hello", mapping={"a": 1, "b": 2, "c": 3})
print(result)
val = client.hgetall("hello")
print(val)
val = client.hget("hello", "a")
print(f"The value of 'a' is {val}")
client.delete("hello")
print(80*"-")


client.hset("boba", mapping={"age": 36, "name": "Boba Fett"})
boba = client.hgetall("boba")
print(type(boba["name"]), type(boba["age"]))
print(80*"-")


# -----------

def insert(minute_of_day: int, measurement: str):
    client.zadd("metrics", {measurement: minute_of_day})


insert(0, "25.0")
insert(1, "26.1")
insert(2, "22.1")
insert(3, "25.0")

print(client.zrange("metrics", 0, -1, withscores=True))
client.unlink("metrics")

# -----------


def run_transaction():
    client.set("a", "foo")
    client.set("b", "bar")
    client.set("c", "baz")

    pipeline = client.pipeline()
    pipeline.set("b", 1)
    pipeline.set("c", "100")
    pipeline.incr("a")

    r1, r2, r3 = pipeline.execute()  # Show error
    print(r1, r2, r3)


# run_transaction()

client.close()