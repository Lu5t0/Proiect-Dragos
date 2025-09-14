import csv

from fastapi import APIRouter, HTTPException, Depends
from routers.auth import  authenticate_user, AuthData

router = APIRouter(prefix="/cars", tags=["Cars"],dependencies=[Depends(authenticate_user)] )
cars_list = "db/cars.csv"
@router.get("")
def get_all_cars():
    with open(cars_list, "r", newline="", encoding="utf-8") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        cars = list(csv_dict_reader)
        for car in cars:
            car.pop("id")
        return cars

@router.post("/add")
def add_car(manufacturer: str, model: str, year: str, transmission: str):
    field_names = ["id", "manufacturer", "model", "year", "transmission"]

    with open(cars_list, "r+", newline="", encoding="utf-8") as csvfile:
        csvfile.seek(0)
        lines = len(csvfile.readlines())

        csv_dict_writer = csv.DictWriter(csvfile, fieldnames=field_names)
        csv_dict_writer.writerow({"id": lines, "manufacturer": manufacturer, "model": model, "year": year, "transmission": transmission})
        return "Added car successfully"
