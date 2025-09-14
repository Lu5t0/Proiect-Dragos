from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,EmailStr
import json

router = APIRouter(prefix="/user", tags=["User"])
User_FILE = "db/users.json"


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

def read_users():
    try:
        with open(User_FILE,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_users(users_list):
    with open(User_FILE,"w") as f:
        json.dump(users_list,f)

@router.put("/register")
def register_user(user : User):
    user_list = read_users()
    for u in user_list:
        if u.get("email", "").lower() == user.email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    user_list.append(new_user)
    write_users(user_list)
    return {"message": "User registered successfully"}