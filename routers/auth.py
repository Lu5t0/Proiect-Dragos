from fastapi import APIRouter, HTTPException,Depends,status
from pydantic import BaseModel,EmailStr
import json

router = APIRouter(prefix="/user", tags=["User"])
User_FILE = "db/users.json"

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class AuthData(BaseModel):
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

def authenticate_user(auth: AuthData = Depends()):
    users = read_users()
    for user in users:
        if user["email"].lower() == auth.email.lower() and user["password"] == auth.password:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

@router.post("/register")
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

@router.post("/login")
def login_user(credentials: AuthData):
    user_list = read_users()
    for u in user_list:
        if u.get("email").lower() == credentials.email.lower() and u.get("password").lower() == credentials.password.lower():
            logged_in_user = u
            return {"message": f"Login Successful for {logged_in_user["email"]}"}

    raise HTTPException(status_code=401, detail="Invalid credentials")




# @router.get("/data")
# def protected_data(user: dict = Depends(authenticate_user)):
#     return {"message": f"Successfully logged in with {user['email']}"}
