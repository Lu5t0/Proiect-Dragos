import csv
from fastapi import APIRouter, HTTPException
from routers.auth import  authenticate_user
from pydantic import BaseModel

router = APIRouter(prefix="/cars", tags=["Cars"])
cars_list = "db/cars.csv"
class Cars(BaseModel):
    manufacturer: str
    model: str
    year: str
    transmission: str
    price_per_day_usd: str

@router.get("")
def get_all_cars(email: str, password: str):
    user = authenticate_user(email,password)
    with open(cars_list, "r", newline="", encoding="utf-8") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        cars = list(csv_dict_reader)
        return cars

@router.post("/add")
def add_car(email: str, password: str, cars: Cars):
    user = authenticate_user(email, password)
    field_names = ["id", "manufacturer", "model", "year", "transmission", "price_per_day_usd","available"]

    with open(cars_list, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        last_id = max(int(row["id"]) for row in rows)

    new_id = last_id + 1

    with open(cars_list, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=field_names, lineterminator="\n")
            writer.writerow({
                "id": new_id,
                "manufacturer": cars.manufacturer,
                "model": cars.model,
                "year": cars.year,
                "transmission": cars.transmission,
                "price_per_day_usd": cars.price_per_day_usd,
                "available": True
            })
            return {"message":"Added car successfully"}

@router.get("/search")
def cars_by_model(email: str, password: str,model: str):
    user = authenticate_user(email, password)
    with open(cars_list, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cars = list(reader)

    result = [car for car in cars if model.lower() in car["model"].lower()]

    if not  result:
        raise HTTPException(status_code=404, detail="No cars found with that model")

    return result
