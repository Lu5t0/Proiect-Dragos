# pip install "fastapi[standard]"
# uvicorn main:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI
from routers import login_router
from routers import register_router
from routers import auth_router


app = FastAPI()
app.include_router(register_router)
app.include_router(login_router)
app.include_router(auth_router)

