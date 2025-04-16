from datetime import date

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI()

user_db = {}

USERNAME_REGEX = r'^[A-Za-z]+$'

class UserBirthdate(BaseModel):
    dateOfBirth: date

@app.put("/hello/{username}", status_code=204)
def put_user_birthdate(
    username: str = Path(..., regex=USERNAME_REGEX),
    data: UserBirthdate = None
):
    if data.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="dateOfBirth must be before today")

    user_db[username] = data.dateOfBirth

    return  # 204 No Content

@app.get("/hello/{username}")
def get_hello(username: str = Path(..., regex=USERNAME_REGEX)):
    if username not in user_db:
        raise HTTPException(status_code=404, detail="User not found")

    dob = user_db[username]
    today = date.today()

    birthday_this_year = dob.replace(year=today.year)

    if birthday_this_year < today:
        birthday_this_year = dob.replace(year=today.year + 1)

    delta = (birthday_this_year - today).days

    if delta == 0:
        return {
            "message": f"Hello, {username}! Happy birthday!"
        }
    else:
        return {
            "message": f"Hello, {username}! Your birthday is in {delta} day(s)"
        }
