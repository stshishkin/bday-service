from datetime import date
from os import environ

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import Column, Date, String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

USERNAME_REGEX = r'^[A-Za-z]+$'
DATABASE_URL = environ.get("DATABASE_URL", "postgresql+asyncpg://user:password@host:5432/dbname")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    date_of_birth = Column(Date, nullable=False)

class UserBirthdate(BaseModel):
    dateOfBirth: date

@app.put("/hello/{username}", status_code=204)
async def put_user_birthdate(
    username: str = Path(..., pattern=USERNAME_REGEX),
    data: UserBirthdate = None
):
    if data.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="dateOfBirth must be before today")

    async with AsyncSessionLocal() as session:
        user = await session.get(User, username)

        if user is None:
            user = User(username=username, date_of_birth=data.dateOfBirth)
            session.add(user)
        else:
            user.date_of_birth = data.dateOfBirth

        await session.commit()

    return  # 204 No Content

@app.get("/hello/{username}")
async def get_hello(username: str = Path(..., pattern=USERNAME_REGEX)):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    dob = user.date_of_birth

    today = date.today()

    try:
        birthday_this_year = dob.replace(year=today.year)
    except ValueError:
        birthday_this_year = dob.replace(year=today.year, month=3, day=1)

    if birthday_this_year < today:
        birthday_this_year = birthday_this_year.replace(year=today.year + 1)

    delta = (birthday_this_year - today).days

    if delta == 0:
        return {
            "message": f"Hello, {username}! Happy birthday!"
        }
    else:
        return {
            "message": f"Hello, {username}! Your birthday is in {delta} day(s)"
        }
