import csv
from fastapi import APIRouter
from routers.auth import  authenticate_user

router = APIRouter(prefix="/stats", tags=["Stats"])
loans_list = "db/loans.csv"
cars_list = "db/cars.csv"

@router.get("/top-cars")
def top_cars(email: str, password: str):
    user = authenticate_user(email, password)

    try:
        with open(loans_list, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            car_ids = [row["car_id"] for row in reader]
    except FileNotFoundError:
        return {"message": "No loan data available"}

    if not car_ids:
        return {"message": "No loans found."}

    counts = {}
    for car_id in car_ids:
        counts[car_id] = counts.get(car_id, 0) + 1

    sorted_cars = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    top_cars_ids = [car_id for car_id, _ in sorted_cars[:5]]

    cars_info = {}

    try:
        with open(cars_list, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cars_info[row["id"]] = row
    except FileNotFoundError:
        return {"message": "Car data file not found."}
    top_cars_details = []
    for car_id in top_cars_ids:
        car = cars_info.get(car_id)
        if car:
            top_cars_details.append({
                "car_id": car_id,
                "manufacturer": car["manufacturer"],
                "model": car["model"],
                "year": car["year"],
                "transmission": car["transmission"],
                "times_rented": counts[car_id],
            })


    return {"top_cars": top_cars_details}