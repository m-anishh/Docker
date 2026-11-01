import pytest
from fastapi.testclient import TestClient
from redis.exceptions import RedisError

import app as app_module


@pytest.fixture
def client(monkeypatch):
    """Use a fake Redis database for fast tests."""

    class FakeRedis:
        def __init__(self):
            self.visits = 0

        def ping(self):
            return True

        def incr(self, key):
            self.visits += 1
            return self.visits

    monkeypatch.setattr(
        app_module, "redis_client", FakeRedis()
    )

    with TestClient(app_module.app) as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Docker project" in response.json()["message"]


def test_health(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_visit_counter(client):
    first = client.get("/visits")
    second = client.get("/visits")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["total_visits"] == 1
    assert second.json()["total_visits"] == 2


def test_redis_failure(client, monkeypatch):
    class BrokenRedis:
        def ping(self):
            raise RedisError("Redis unavailable")

        def incr(self, key):
            raise RedisError("Redis unavailable")

    monkeypatch.setattr(
        app_module, "redis_client", BrokenRedis()
    )

    assert client.get("/healthz").status_code == 503
    assert client.get("/visits").status_code == 503

def test_health_failure_message(client, monkeypatch):
    class UnavailableRedis:
        def ping(self):
            raise RedisError("Connection refused")

    monkeypatch.setattr(
        app_module, "redis_client", UnavailableRedis()
    )

    response = client.get("/healthz")
    assert response.status_code == 503
    assert response.json() == {"detail": "Redis unavailable"}
