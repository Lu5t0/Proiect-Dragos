from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel,EmailStr
import json

router = APIRouter(prefix="/user", tags=["User"])

User_FILE = "db/users.json"

logged_in_user = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def read_users():
    try:
        with open(User_FILE,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@router.post("/login")
def login_user(credentials: LoginRequest):
    global logged_in_user
    user_list = read_users()
    for u in user_list:
        if u.get("email").lower() == credentials.email.lower() and u.get("password").lower() == credentials.password.lower():
            logged_in_user = u
            return {"message": f"Login Successful for {logged_in_user["email"]}"}

    raise HTTPException(status_code=401, detail="Invalid credentials")

def verify_logged_in_user():
    global logged_in_user
    if logged_in_user is None:
        raise HTTPException(status_code=401, detail="you are not logged in!")

# @router.get("/protected-route")
# def protected_route():
#     verify_logged_in()
#     return {"message": f"Acces permis pentru {logged_in_user}"}

@router.post("/logout")
def logout():
    global logged_in_user
    logged_in_user = None
    return {"message": "You have been logged out!"}