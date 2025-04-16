import os
import pytest
import asyncio
from datetime import date
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

from bday_service.app import app, Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    async def init_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_tables())

    yield

    if os.path.exists("test.db"):
        os.remove("test.db")

client = TestClient(app)

def test_put_user_correct():
    username = "John"
    dob = "1990-01-01"
    response = client.put(f"/hello/{username}", json={"dateOfBirth": dob})
    assert response.status_code == 204

    response = client.get(f"/hello/{username}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_put_user_invalid():
    username = "John123"
    dob = "1990-01-01"
    response = client.put(f"/hello/{username}", json={"dateOfBirth": dob})
    assert response.status_code == 422

def test_put_user_invalid_date():
    username = "Alice"
    today_str = date.today().strftime("%Y-%m-%d")
    response = client.put(f"/hello/{username}", json={"dateOfBirth": today_str})
    assert response.status_code == 400

def test_put_user_leap_year():
    username = "LeapYear"
    dob = "2020-02-29"
    response = client.put(f"/hello/{username}", json={"dateOfBirth": dob})
    assert response.status_code == 204

    response = client.get(f"/hello/{username}")
    assert response.status_code == 200
    assert "message" in response.json()
