import csv
from fastapi import APIRouter, HTTPException
from routers.auth import  authenticate_user
from pydantic import BaseModel

router = APIRouter(prefix="/cars", tags=["Cars"])
cars_list = "db/cars.csv"
manu_list = "db/manufacturer.csv"
class Cars(BaseModel):
    manufacturer: str
    model: str
    year: str
    transmission: str
    price_per_day_usd: str

@router.get("")
def get_all_cars():
    with open(cars_list, "r", newline="", encoding="utf-8") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        cars = list(csv_dict_reader)
        return cars

@router.post("/add")
def add_car(email: str, password: str, cars: Cars):
    user = authenticate_user(email, password)

    with open(manu_list, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        valid_manu = [row["name"].lower() for row in reader]

        if cars.manufacturer.lower() not in valid_manu:
            raise HTTPException(
                status_code=400,
                detail = f"Manufacturer {cars.manufacturer} is not registered."
            )

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
def cars_by_model(model: str):
    with open(cars_list, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cars = list(reader)

    result = [car for car in cars if model.lower() in car["model"].lower()]

    if not  result:
        raise HTTPException(status_code=404, detail="No cars found with that model")

    return result
