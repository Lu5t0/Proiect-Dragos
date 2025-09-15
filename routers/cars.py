import csv

from fastapi import APIRouter, HTTPException
from routers.auth import  authenticate_user
from pydantic import BaseModel

router = APIRouter(prefix="/cars", tags=["Cars"])
cars_list = "db/cars.csv"

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("")
def get_all_cars(data: LoginRequest):
    user = authenticate_user(data.email, data.password)
    with open(cars_list, "r", newline="", encoding="utf-8") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        cars = list(csv_dict_reader)
        for car in cars:
            car.pop("id")
        return cars

@router.post("/add")
def add_car(data: LoginRequest, manufacturer: str, model: str, year: str, transmission: str):
    user = authenticate_user(data.email, data.password)
    field_names = ["id", "manufacturer", "model", "year", "transmission"]

    with open(cars_list, "r+", newline="", encoding="utf-8") as csvfile:
        csvfile.seek(0)
        lines = len(csvfile.readlines())

        csv_dict_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_dict_writer.writerow({"id": lines, "manufacturer": manufacturer, "model": model, "year": year, "transmission": transmission})
        return "Added car successfully"
