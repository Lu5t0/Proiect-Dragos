from fastapi import APIRouter, HTTPException,Depends,status
from pydantic import BaseModel,EmailStr
import json

router = APIRouter(prefix="/user", tags=["User"])

class AuthData(BaseModel):
    email: EmailStr
    password: str

def read_users():
    try:
        with open(User_FILE,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def authenticate_user(auth: AuthData = Depends()):
    users = read_users()
    for user in users:
        if user["email"] == auth.email and user["password"] == auth.password:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

# @router.get("/data")
# def protected_data(user: dict = Depends(authenticate_user)):
#     return {"message": f"Successfully logged in with {user['email']}"}