# pip install "fastapi[standard]"
# uvicorn main:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI
from routers import auth_router
from routers import cars_router
from routers import manufacturer_router
from routers import loan_router
from routers import stats_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(cars_router)
app.include_router(manufacturer_router)
app.include_router(loan_router)
app.include_router(stats_router)
