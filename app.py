import os
from fastapi import FastAPI, HTTPException
from redis import Redis
from redis.exceptions import RedisError

app = FastAPI(title="Docker Visitor Counter")

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.get("/")
def home():
    return {"message": "Welcome to my first Docker project!"}

@app.get("/healthz")
def health():
    try:
        redis_client.ping()
        return {"status": "healthy"}
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

@app.get("/visits")
def count_visits():
    try:
        count = redis_client.incr("visits")
        return {"total_visits": count}
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")
